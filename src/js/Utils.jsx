import colors from 'config/colors';

export function parseJsonPromise(text) {
  return new Promise((resolve, reject) => {
    try {
      resolve(JSON.parse(text));
    } catch (err) {
      reject(err);
    }
  });
}

// https://stackoverflow.com/a/6610501/1480571
export function withoutScrolling(thunk) {
  const x = window.scrollX, y = window.scrollY;
  thunk();
  window.scrollTo(x, y);
}

export function pickColorFromString(s) {
  let num = 0;
  for (let i = 0; i < s.length; i++) {
    num = (num + s.charCodeAt(i)) % colors.length;
  }
  return colors[num];
}

// Non-breaking space
export const nbsp = '\u00a0';

