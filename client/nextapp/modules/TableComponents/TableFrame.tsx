import { type ReactNode } from 'react'
import { useRouter } from 'next/router'
import { type ColumnInstance } from 'react-table'
import useMedia from '@charlietango/use-media'
import clsx from 'clsx'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useQuery } from '@tanstack/react-query'

import { animated, useSpring } from '@react-spring/web'
import { ToastContainer } from 'react-toastify'
import Select from 'modules/Select'
import Button from 'modules/Button'
import { CustomizeColumnsDrawer, type DrawerExtensionTypes } from './CustomizeColumnsDrawer'
import { GlobalTextFilter } from './GlobalTextFilter'
import { ToggleCustomizeOrder } from './ToggleCustomizeOrder'
import { Pagination } from './Pagination'

export type TableFrameProps<TTableFrameColumnInstance extends object> = {
  children: ReactNode
  pageCount: number
  pageSize: number
  totalNumber: number
  pageOptions: number[]
  pageIndex: number
  tableType: 'flight' | 'mission' | 'drone'
  drawerExtensionType: DrawerExtensionTypes
  groupByOptions: { name: string; value: string }[]
  allColumns: ColumnInstance<TTableFrameColumnInstance>[]
  setColumnOrder: (updater: string[] | ((columnOrder: string[]) => string[])) => void
  setGlobalFilter: (filterValue: string) => void
  globalFilter: string
  setGroupBy: (value: [string]) => void
  width?: number
}

export const TableFrame = <TTableFrameColumnInstance extends object>({
  children,
  pageCount,
  pageSize,
  totalNumber,
  pageOptions,
  pageIndex,
  tableType,
  drawerExtensionType,
  groupByOptions,
  allColumns,
  setColumnOrder,
  setGlobalFilter,
  setGroupBy,
  globalFilter,
  width,
}: TableFrameProps<TTableFrameColumnInstance>) => {
  const router = useRouter()
  const matches = useMedia({ minWidth: 1920 })

  const { data: sideNavExtended } = useQuery([drawerExtensionType], () => {
    return false
  })

  const slideX = useSpring({
    transform: sideNavExtended ? 'translate3d(20px,0,0)' : `translate3d(-240px,0,0)`,
    minWidth: sideNavExtended ? 'calc(100vw - 270px)' : `calc(100vw - 0px)`,
  })

  return (
    <div
      className={`flex-column
                  flex
                  min-h-screen
                  
                `}
    >
      <ToastContainer />
      <CustomizeColumnsDrawer
        allColumns={allColumns}
        setColumnOrder={setColumnOrder}
        drawerKey={drawerExtensionType}
      />
      <animated.div
        className={clsx(`ml-side-drawer-width
                         h-screen
                         overflow-x-hidden
                         px-12`)}
        style={slideX}
      >
        <div
          style={
            width
              ? {
                  maxWidth: matches ? width + 40 : '100%',
                }
              : {}
          }
          className={`
                      relative
                      mx-auto                     
                      mb-40
                      pl-2
                      pr-8
                      pt-20
                      pb-12`}
        >
          <div
            className={`mb-4
                        grid
                        grid-cols-[minmax(700px,_1fr)_200px]
                        grid-rows-2
                        items-end
                        gap-y-2
                        gap-x-8`}
          >
            <GlobalTextFilter globalFilter={globalFilter} setGlobalFilter={setGlobalFilter} />

            <Select
              name="groupby"
              placeholder="Group by"
              options={groupByOptions}
              onSetValue={setGroupBy}
              defaultValue="None"
              hasResetButton={true}
              resetButtonText={'Reset Group'}
            />
          </div>
          <div className="flex">
            <div
              className={`pr-4
                          pt-4`}
            >
              <Button
                isSpecial={true}
                buttonStyle="Main"
                className={`w-[200px]
                            px-6
                            py-3`}
                onClick={async () => {
                  await router.push(
                    `/add/${tableType}?curentPageSize=${pageSize}&currentPageCount=${pageCount}&totalNumber=${totalNumber}`,
                  )
                }}
              >
                <FontAwesomeIcon icon={'plus-circle'} height="32" className="scale-150" />
                <span className="ml-3">{`Add new ${tableType}`}</span>
              </Button>
            </div>
            <ToggleCustomizeOrder drawerKey={drawerExtensionType} />
          </div>

          {children}

          <Pagination
            pageSize={pageSize}
            pageCount={pageCount}
            pageIndex={pageIndex}
            pageOptions={pageOptions}
            totalNumber={totalNumber}
          />
        </div>

        <div
          className={`mb-4
                        grid
                        grid-cols-[minmax(700px,_1fr)_200px]
                        grid-rows-2
                        items-end
                        gap-y-2
                        gap-x-8`}
        ></div>
      </animated.div>
    </div>
  )
}
