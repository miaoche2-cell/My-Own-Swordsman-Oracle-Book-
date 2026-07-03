import { useState } from 'react'
import useBookStore from '../store/bookStore'
import coverConfig from '../data/coverConfig.json'
import styles from './CoverPage.module.css'

export default function CoverPage() {
  const openBook = useBookStore((s) => s.openBook)
  const [opening, setOpening] = useState(false)
  const [fading, setFading] = useState(false)

  const handleClick = () => {
    if (opening) return
    setOpening(true)

    // 翻书动画 800ms → 整体淡出 200ms → 切换页面
    setTimeout(() => setFading(true), 800)
    setTimeout(() => openBook(), 1000)
  }

  return (
    <div className={`${styles.cover} ${fading ? styles.fading : ''}`}>
      {/* 桌面背景 */}
      <div className={styles.desk} />

      {/* 光晕 */}
      <div className={styles.glow} />

      {/* 3D 翻书场景 */}
      <div className={styles.bookScene}>
        <div className={`${styles.book} ${opening ? styles.opening : ''}`} onClick={handleClick}>
          {/* 线装书脊 */}
          <div className={styles.binding}>
            <div className={styles.threadHole} />
            <div className={styles.threadLine} />
            <div className={styles.threadHole} />
            <div className={styles.threadLine} />
            <div className={styles.threadHole} />
            <div className={styles.threadLine} />
            <div className={styles.threadHole} />
          </div>

          {/* 书页 + 封面堆叠 */}
          <div className={styles.bookBlock}>
            {/* 内页堆叠 — 封面翻开后可见 */}
            <div className={styles.pagesStack}>
              {/* 左半页（封面下） */}
              <div className={styles.pageLeft} />
              <div className={styles.pageLeft} />
              <div className={styles.pageLeft} />
              <div className={styles.pageLeft} />
              {/* 右半页（书的另一侧） */}
              <div className={styles.pageRight} />
              <div className={styles.pageRight} />
              <div className={styles.pageRight} />
              <div className={styles.pageRight} />
            </div>

            {/* 书页中缝阴影 */}
            <div className={styles.gutterShadow} />

            {/* 书封（最上层，翻动） */}
            <div className={styles.coverBody}>
              <div className={styles.coverBorder}>
                <div className={styles.coverInner}>
                  <div className={styles.logoWrap}>
                    <img
                      src={coverConfig.logo.src}
                      alt={coverConfig.logo.alt}
                      className={styles.logo}
                    />
                  </div>
                  <p className={styles.subtitle}>{coverConfig.subtitle}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 底部提示 */}
      <p className={`${styles.hint} ${opening ? styles.hiding : ''}`}>
        {coverConfig.hint}
      </p>

      {/* 设计者 */}
      <p className={`${styles.designer} ${opening ? styles.hiding : ''}`}>
        design by 姜鬼
      </p>

      {/* 飘浮粒子 */}
      <div className={styles.particles}>
        {[...Array(6)].map((_, i) => (
          <span key={i} className={styles.particle} style={{
            left: `${10 + Math.random() * 80}%`,
            animationDelay: `${Math.random() * 8}s`,
            animationDuration: `${8 + Math.random() * 12}s`,
          }} />
        ))}
      </div>
    </div>
  )
}
