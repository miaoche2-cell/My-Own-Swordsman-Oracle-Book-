import { create } from 'zustand'

const useBookStore = create((set, get) => ({
  // 状态：'cover' | 'answer'
  page: 'cover',

  // 答案数据
  answers: [],

  // 当前显示的答案
  currentAnswer: null,

  // 上次显示的答案索引列表（用于去重）
  recentIndices: [],

  setAnswers: (answers) => set({ answers }),
  setCurrentAnswer: (currentAnswer) => set({ currentAnswer }),

  // 翻开答案之书
  openBook: () => {
    const { answers, recentIndices } = get()
    if (!answers.length) return

    // 随机选一条，避免最近5条重复
    const maxRecent = Math.min(5, answers.length - 1)
    let index
    do {
      index = Math.floor(Math.random() * answers.length)
    } while (recentIndices.includes(index) && recentIndices.length < answers.length)

    const newRecent = [...recentIndices, index].slice(-maxRecent)

    set({
      page: 'answer',
      currentAnswer: answers[index],
      recentIndices: newRecent,
    })
  },

  // 返回封面，再问一次
  backToCover: () => set({ page: 'cover', currentAnswer: null }),
}))

export default useBookStore
