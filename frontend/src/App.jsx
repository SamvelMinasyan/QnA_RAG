// import React, { useState } from 'react'
// import ReactDOM from 'react-dom/client'
// import { ask } from './api'
//
// function App() {
//   // Local state for question input, answer, and history
//   const [question, setQuestion] = useState('')
//   const [answer, setAnswer] = useState('')
//   const [history, setHistory] = useState([])
//
//   const handleAsk = async () => {
//     if (!question.trim()) {
//       setAnswer('Please enter a question.')
//       return
//     }
//     try {
//       // Call backend ask endpoint
//       const data = await ask(question)
//       setAnswer(data.answer)
//       setHistory(prev => [...prev, { q: data.question, a: data.answer }])
//     } catch (err) {
//       setAnswer(`Error: ${err.message}`)
//     }
//   }
//
//   return (
//     <div className="app-container">
//       <h1>AI-Powered Q&A</h1>
//       <input
//         type="text"
//         value={question}
//         onChange={e => setQuestion(e.target.value)}
//         placeholder="Ask a question..."
//       />
//       <button onClick={handleAsk}>Ask</button>
//
//       <section>
//         <h2>Answer:</h2>
//         <p>{answer}</p>
//       </section>
//
//       <section>
//         <h2>History</h2>
//         <ul>
//           {history.map((h, i) => (
//             <li key={i}><strong>{h.q}</strong>: {h.a}</li>
//           ))}
//         </ul>
//       </section>
//     </div>
//   )
// }
//
// const root = ReactDOM.createRoot(document.getElementById('root'))
// root.render(<App />)

import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'
import { ask, summarize } from './api'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [summary, setSummary] = useState('')
  const [history, setHistory] = useState([])

  const handleAsk = async () => {
    if (!question.trim()) {
      setAnswer('Please enter a question.')
      return
    }
    try {
      const data = await ask(question)
      setAnswer(data.answer)
      setHistory(prev => [...prev, { q: data.question, a: data.answer }])
      setSummary('')  // clear any previous summary
    } catch (err) {
      setAnswer(`Error: ${err.message}`)
    }
  }

  const handleSummarize = async () => {
    if (!answer) return
    try {
      const sum = await summarize(answer)
      setSummary(sum)
    } catch (err) {
      setSummary(`Error: ${err.message}`)
    }
  }

  return (
    <div className="app-container">
      <h1>AI-Powered Q&A</h1>
      <input
        type="text"
        value={question}
        onChange={e => setQuestion(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={handleAsk}>Ask</button>

      <section>
        <h2>Answer:</h2>
        <p>{answer}</p>
        {answer && (
          <button onClick={handleSummarize} style={{ marginTop: 8 }}>
            Summarize
          </button>
        )}
        {summary && (
          <div style={{ marginTop: 12, padding: 8, background: '#f0f0f0', borderRadius: 4 }}>
            <h3>Summary:</h3>
            <p>{summary}</p>
          </div>
        )}
      </section>

      <section>
        <h2>History</h2>
        <ul>
          {history.map((h, i) => (
            <li key={i}><strong>{h.q}</strong>: {h.a}</li>
          ))}
        </ul>
      </section>
    </div>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(<App />)
