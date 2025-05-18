// export async function ask(question) {
//   const res = await fetch('http://localhost:8000/api/ask', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ question })
//   });
//   return res.json();
// }
export async function ask(question) {
  const res = await fetch('http://localhost:8000/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}

export async function summarize(answer) {
  const res = await fetch('http://localhost:8000/api/summarize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answer })
  });
  if (!res.ok) throw new Error(`Error ${res.status}`);
  const { summary } = await res.json();
  return summary;
}
