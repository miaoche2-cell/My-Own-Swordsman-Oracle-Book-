import { useEffect } from 'react'
import useBookStore from './store/bookStore'
import CoverPage from './components/CoverPage'
import AnswerPage from './components/AnswerPage'
import answers from './data/answers.json'

export default function App() {
  const page = useBookStore((s) => s.page)
  const setAnswers = useBookStore((s) => s.setAnswers)

  useEffect(() => {
    setAnswers(answers)
  }, [setAnswers])

  return page === 'cover' ? <CoverPage /> : <AnswerPage />
}
