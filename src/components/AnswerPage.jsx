import { useEffect, useState } from 'react'
import useBookStore from '../store/bookStore'
import coverConfig from '../data/coverConfig.json'
import styles from './AnswerPage.module.css'

// 角色名 → 头像文件名映射
const AVATAR_MAP = {
  '佟湘玉': '佟湘玉.JPG',
  '白展堂': '白展堂.JPG',
  '郭芙蓉': '郭芙蓉.JPG',
  '吕秀才': '吕秀才.JPG',
  '李大嘴': '李大嘴.JPG',
  '莫小贝': '莫小贝.JPG',
  '祝无双': '祝无双.JPG',
  '燕小六': '燕小六.JPG',
  '邢育森': '邢育森.JPG',
}

function getAvatarPath(character) {
  // 精确匹配
  if (AVATAR_MAP[character]) {
    return `/images/avatars/${AVATAR_MAP[character]}`
  }
  // 合体角色如 "佟湘玉/白展堂" → 取第一个
  if (character.includes('/')) {
    const first = character.split('/')[0].trim()
    if (AVATAR_MAP[first]) {
      return `/images/avatars/${AVATAR_MAP[first]}`
    }
  }
  return null
}

export default function AnswerPage() {
  const currentAnswer = useBookStore((s) => s.currentAnswer)
  const backToCover = useBookStore((s) => s.backToCover)
  const [visible, setVisible] = useState(false)
  const [imgError, setImgError] = useState(false)
  // 用于强制重播头像动画
  const [animKey, setAnimKey] = useState(0)

  useEffect(() => {
    setImgError(false)
    setAnimKey(k => k + 1)
    const timer = setTimeout(() => setVisible(true), 100)
    return () => clearTimeout(timer)
  }, [currentAnswer])

  if (!currentAnswer) return null

  const avatarPath = getAvatarPath(currentAnswer.character)
  const hasAvatar = avatarPath && !imgError

  return (
    <div className={`${styles.page} ${visible ? styles.visible : ''}`}>
      {/* 桌面背景 */}
      <div className={styles.desk} />

      {/* 古籍翻开 */}
      <div className={styles.bookSpread}>
        {/* 左页：人物头像 */}
        <div className={styles.leftPage}>
          <div className={styles.avatarWrap} key={animKey}>
            {hasAvatar ? (
              <>
                {/* 头像金晕特效 */}
                <div className={styles.avatarGlow} />
                <img
                  src={avatarPath}
                  alt={currentAnswer.character}
                  className={styles.avatarImg}
                  onError={() => setImgError(true)}
                />
              </>
            ) : (
              <img
                src={coverConfig.logo.src}
                alt={coverConfig.logo.alt}
                className={styles.avatarPlaceholder}
              />
            )}
          </div>
        </div>

        {/* 右页：正文 + 出处 */}
        <div className={styles.rightPage}>
          <blockquote className={styles.quote}>
            {currentAnswer.quote}
          </blockquote>
          <div className={styles.source}>
            <span className={styles.episodeLabel}>
              {currentAnswer.episode}
            </span>
            <span className={styles.episodeTitle}>
              {currentAnswer.episodeTitle}
            </span>
          </div>
        </div>
      </div>

      {/* 操作按钮 */}
      <div className={styles.actions}>
        <button className={styles.btnBack} onClick={backToCover}>
          合上书
        </button>
      </div>
    </div>
  )
}
