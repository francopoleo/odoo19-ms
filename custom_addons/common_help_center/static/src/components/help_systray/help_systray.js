/** @odoo-module **/

import { Component, markup, onWillUnmount, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class HelpCenterSystray extends Component {
    setup() {
        this.action = useService("action");
        this.notification = useService("notification");
        this.orm = useService("orm");
        this.state = useState({
            open: false,
            loading: false,
            query: "",
            bundle: { articles: [], tips: [], checklists: [], suggestions: [], context: {} },
            errorSuggestions: [],
            selectedArticle: null,
            selectedArticleLoading: false,
        });
        this._errorListener = async (event) => {
            try {
                const text = this._errorToText(event.reason || event.error || event.message || event);
                if (!text || text.length < 15) {
                    return;
                }
                const suggestions = await this.orm.call("help.article", "get_error_suggestions", [], {
                    error_text: text,
                    context_info: this._getCurrentActionContext(),
                });
                if (suggestions && suggestions.length) {
                    this.state.errorSuggestions = suggestions;
                    this.notification.add("A Central de Ajuda encontrou sugestões para o erro ocorrido.", {
                        type: "warning",
                    });
                }
            } catch (error) {
                // Nunca quebrar a interface por causa da ajuda.
                console.warn("Central de Ajuda: falha ao analisar erro", error);
            }
        };
        window.addEventListener("unhandledrejection", this._errorListener);
        window.addEventListener("error", this._errorListener);
        onWillUnmount(() => {
            window.removeEventListener("unhandledrejection", this._errorListener);
            window.removeEventListener("error", this._errorListener);
        });
    }

    _errorToText(error) {
        if (!error) {
            return "";
        }
        if (typeof error === "string") {
            return error;
        }
        if (error.message) {
            return `${error.message}\n${error.stack || ""}`;
        }
        try {
            return JSON.stringify(error);
        } catch (_) {
            return String(error);
        }
    }

    _getCurrentActionContext() {
        const controller = this.action.currentController || {};
        const action = controller.action || {};
        const props = controller.props || {};
        const model = controller.model || {};
        const root = model.root || {};
        const config = model.config || {};
        const actionContext = action.context || {};

        let resModel =
            action.res_model ||
            props.resModel ||
            props.res_model ||
            props.archInfo?.resModel ||
            controller.resModel ||
            controller.modelName ||
            config.resModel ||
            config.res_model ||
            root.resModel ||
            actionContext.active_model ||
            false;

        let viewType =
            props.viewType ||
            props.type ||
            controller.view?.type ||
            controller.viewType ||
            config.viewType ||
            action.views?.[0]?.[1] ||
            false;

        let resId =
            props.resId ||
            props.res_id ||
            controller.resId ||
            root.resId ||
            root.res_id ||
            actionContext.active_id ||
            false;

        // Fallback útil no Odoo 19: algumas rotas incluem o model no path,
        // por exemplo /odoo/action-209/15/governance.case?debug=1.
        if (!resModel) {
            const match = (window.location.pathname || '').match(/\/([a-zA-Z_][\w]*(?:\.[a-zA-Z_][\w]*)+)\/?$/);
            if (match) {
                resModel = match[1];
            }
        }

        if (!viewType && resId) {
            viewType = 'form';
        }
        if (!viewType) {
            viewType = 'list';
        }

        return {
            resModel,
            viewType,
            resId,
            menuXmlid: action.menu_xmlid || actionContext.menu_xmlid || false,
            actionXmlid: action.xml_id || action.xmlid || actionContext.action_xmlid || false,
            actionId: action.id || false,
        };
    }

    async openHelpDrawer(ev) {
        if (ev) {
            ev.preventDefault();
            ev.stopPropagation();
        }
        this.state.open = true;
        await this.loadBundle();
    }

    closeHelpDrawer() {
        this.state.open = false;
        this.state.selectedArticle = null;
    }

    backToContext() {
        this.state.selectedArticle = null;
    }

    async loadBundle() {
        this.state.loading = true;
        try {
            const bundle = await this.orm.call("help.article", "get_context_bundle", [], {
                context_info: this._getCurrentActionContext(),
                query: this.state.query || false,
            });
            this.state.bundle = bundle || { articles: [], tips: [], checklists: [], suggestions: [], context: {} };
            this.state.selectedArticle = null;
        } catch (error) {
            console.error("Erro ao carregar ajuda contextual", error);
            this.notification.add("Não foi possível carregar a ajuda contextual. Abrindo a Central de Ajuda.", {
                type: "warning",
            });
            await this.openHelpCenter();
        } finally {
            this.state.loading = false;
        }
    }

    async searchHelp(ev) {
        if (ev) {
            ev.preventDefault();
        }
        await this.loadBundle();
    }

    async openHelpCenter(ev) {
        if (ev) {
            ev.preventDefault();
            ev.stopPropagation();
        }
        await this.action.doAction({
            type: "ir.actions.act_window",
            name: "Central de Ajuda",
            res_model: "help.article",
            views: [[false, "list"], [false, "form"]],
            target: "current",
            domain: [["published", "=", true]],
            context: { search_default_published: 1 },
        });
        this.closeHelpDrawer();
    }

    async openContextConfiguration(ev) {
        if (ev) {
            ev.preventDefault();
            ev.stopPropagation();
        }
        const ctx = this._getCurrentActionContext();
        await this.action.doAction({
            type: "ir.actions.act_window",
            name: "Configurar ajuda desta tela",
            res_model: "help.context",
            views: [[false, "list"], [false, "form"]],
            target: "current",
            domain: [["model_name", "=", ctx.resModel || false]],
            context: {
                default_name: `Ajuda - ${ctx.resModel || "Tela atual"} ${ctx.viewType || ""}`,
                default_model_name: ctx.resModel || false,
                default_view_type: ctx.viewType || false,
                default_action_xmlid: ctx.actionXmlid || false,
            },
        });
        this.closeHelpDrawer();
    }

    async openArticle(article) {
        if (!article || !article.id) {
            return;
        }
        this.state.selectedArticleLoading = true;
        try {
            await this.orm.call("help.article", "log_article_open", [], {
                article_id: article.id,
                context_info: this._getCurrentActionContext(),
            });
            const result = await this.orm.call("help.article", "get_drawer_article", [], {
                article_id: article.id,
            });
            if (result && result.id) {
                this.state.selectedArticle = {
                    ...result,
                    content: markup(result.content_html || "<p class='text-muted'>Este artigo ainda não possui conteúdo.</p>"),
                };
            }
        } catch (error) {
            console.warn("Erro ao abrir artigo no painel", error);
            this.notification.add("Não foi possível abrir o artigo no painel. Abrindo em tela completa.", { type: "warning" });
            await this.action.doAction({
                type: "ir.actions.act_window",
                name: article.name,
                res_model: "help.article",
                res_id: article.id,
                views: [[false, "form"]],
                target: "current",
            });
            this.closeHelpDrawer();
        } finally {
            this.state.selectedArticleLoading = false;
        }
    }

    async openArticleFull(article) {
        const targetArticle = article || this.state.selectedArticle;
        if (!targetArticle || !targetArticle.id) {
            return;
        }
        await this.action.doAction({
            type: "ir.actions.act_window",
            name: targetArticle.name,
            res_model: "help.article",
            res_id: targetArticle.id,
            views: [[false, "form"]],
            target: "current",
        });
        this.closeHelpDrawer();
    }

    async toggleChecklist(item) {
        if (!item || !item.id) {
            return;
        }
        const ctx = this._getCurrentActionContext();
        try {
            const done = await this.orm.call("help.checklist.progress", "toggle_progress", [
                item.id,
                ctx.resModel || false,
                ctx.resId || 0,
                !item.done,
            ]);
            item.done = done;
        } catch (error) {
            console.warn("Erro ao atualizar checklist", error);
            this.notification.add("Não foi possível atualizar o checklist.", { type: "warning" });
        }
    }

    async sendFeedback(article, rating) {
        if (!article || !article.id) {
            return;
        }
        const ctx = this._getCurrentActionContext();
        try {
            await this.orm.create("help.feedback", [{
                article_id: article.id,
                rating,
                model_name: ctx.resModel || false,
                record_id: ctx.resId || 0,
            }]);
            this.notification.add("Obrigado pelo feedback.", { type: "success" });
        } catch (error) {
            console.warn("Erro ao registrar feedback", error);
        }
    }
}

HelpCenterSystray.template = "common_help_center.HelpCenterSystray";

registry.category("systray").add(
    "common_help_center.help_systray",
    { Component: HelpCenterSystray },
    { sequence: 95 }
);
