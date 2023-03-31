import clsx from 'clsx'
import { TableBodyPropGetter, TableBodyProps as ReactTableBodyProps, Row } from 'react-table'

export type TestProps<TColumnProps extends object> = {
  getTableBodyProps: (
    propGetter?: TableBodyPropGetter<TColumnProps> | undefined,
  ) => ReactTableBodyProps
  page: Row<TColumnProps>[]
  prepareRow: (row: Row<TColumnProps>) => void
  firstColumnAccessor: string
  hasRecords: boolean
}

export const TableBody = <TColumnProps extends object>({
  getTableBodyProps,
  page,
  prepareRow,
  firstColumnAccessor,
  hasRecords,
}: TestProps<TColumnProps>) => {
  if (!hasRecords) {
    return (
      <div
        className={`flex
                    h-[150px]
                    w-full
                    items-center
                    justify-center
                    rounded-lg
                    bg-primary-white`}
      >
        No records found
      </div>
    )
  }

  return (
    <tbody {...getTableBodyProps()} className="min-w-full">
      {page.map((row, index) => {
        prepareRow(row)
        const { key, ...restRowProps } = row.getRowProps()

        const isEven = index % 2 === 0

        return (
          <tr
            {...restRowProps}
            key={key}
            className={clsx(
              `my-2
               flex
               w-full
               rounded-lg
               border-l-[12px]
               bg-primary-white
               text-xs
               transition-opacity
               hover:opacity-60`,
              isEven ? `border-l-primary-dark-petrol` : 'border-l-primary-indigo-blue',
            )}
          >
            {row.cells.map((cell: any, index: number) => {
              const { key, ...restCellProps } = cell.getCellProps()

              return (
                <td
                  {...restCellProps}
                  key={key}
                  className={clsx(
                    `flex
                     items-center
                     justify-center
                     text-center`,
                    cell.column.id === firstColumnAccessor
                      ? `flex 
                         rounded-r-[0px]
                         rounded-l-[0px]
                         rounded-tl-lg
                         rounded-bl-lg
                         px-4
                         last-of-type:align-middle`
                      : `
                         flex
                         items-center
                         justify-center
                         px-4
                         py-6`,
                    !row.isGrouped &&
                      `justify-center
                       text-center`,
                    index === 0
                      ? `ml-4
                         w-[22px]`
                      : '',
                  )}
                >
                  <span className={cell.column.width}>
                    {cell.isGrouped ? (
                      // If it's a grouped cell, add an expander and row count
                      <>
                        <span {...row.getToggleRowExpandedProps()}>
                          {row.isExpanded ? '-' : '+'}
                        </span>
                        {cell.render('Cell')} ({row.subRows.length})
                      </>
                    ) : cell.isAggregated ? (
                      // If the cell is aggregated, use the Aggregated
                      // renderer for cell
                      <span className="w-[200px]">{cell.render('Aggregated')}</span>
                    ) : cell.isPlaceholder ? null : ( // For cells with repeated values, render null
                      // Otherwise, just render the regular cell
                      cell.render('Cell')
                    )}
                  </span>
                </td>
              )
            })}
          </tr>
        )
      })}
    </tbody>
  )
}
