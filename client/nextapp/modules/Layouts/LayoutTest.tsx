/* 
  The following Component is currently not used
 */
import { ReactNode } from 'react'
import { animated, useSpring } from '@react-spring/web'
import clsx from 'clsx'
import { useTranslation } from 'next-i18next'
import { useQuery } from '@tanstack/react-query'
import SideNavigation from 'modules/SideNavigation'
import Header from '~/modules/Header'

const DRAWER_EXTENDED = 'drawer-extended'

export type Props = { children: ReactNode }

export const Layout = ({ children }: Props) => {
  const { t } = useTranslation()
  const { data: sideNavExtended } = useQuery([DRAWER_EXTENDED])

  const slideX = useSpring({
    transform: sideNavExtended ? 'translate3d(0px,0,0)' : `translate3d(-200px,0,0)`,
    minWidth: sideNavExtended ? 'calc(100vw - 270px)' : `calc(100vw - 60px)`,
  })

  return (
    <>
      <div
        className={`flex-column
                    flex
                    min-h-screen`}
      >
        <SideNavigation />
        <animated.div
          className={clsx(`ml-side-drawer-width
                           h-screen
                           overflow-x-hidden`)}
          style={slideX}
        >
          <Header />
          <main
            className={`flex
                        min-h-screen
                        w-full
                        justify-center
                        bg-grey-light
                        `}
          >
            {children}
          </main>
        </animated.div>
      </div>
    </>
  )
}