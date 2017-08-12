export function parseJsonPromise(text) {
  return new Promise((resolve, reject) => {
    try {
      resolve(JSON.parse(text));
    } catch (err) {
      reject(err);
    }
  });
}