// ES2024 Polyfills for older browsers
if (typeof Object.groupBy !== 'function') {
  Object.groupBy = function(items, keyFn) {
    const result = {};
    for (const item of items) {
      const key = keyFn(item);
      if (!result[key]) result[key] = [];
      result[key].push(item);
    }
    return result;
  };
}