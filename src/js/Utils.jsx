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

export function pickColorFromString(s) {
  let num = 0;
  for (let i = 0; i < s.length; i++) {
    num = (num + s.charCodeAt(i)) % colors.length;
  }
  return colors[num];
}

// Non-breaking space
export const nbsp = '\u00a0';

