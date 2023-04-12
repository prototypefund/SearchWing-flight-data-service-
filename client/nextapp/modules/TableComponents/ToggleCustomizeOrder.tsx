import { useQueryClient, useQuery } from '@tanstack/react-query'
import Button from 'modules/Button'
import { DrawerExtensionTypes } from './CustomizeColumnsDrawer'

export const ToggleCustomizeOrder = ({ drawerKey }: { drawerKey: DrawerExtensionTypes }) => {
  const { data: isExtended } = useQuery([drawerKey], () => {
    return false
  })

  const queryClient = useQueryClient()

  const handleToggleDrawer = () => {
    queryClient.setQueryData<boolean>([drawerKey], (prev) => {
      return !prev
    })
  }

  return (
    <div
      className="h-full
                 py-8
                text-primary-white"
    >
      <Button
        id="toggleCustomizeOrder"
        type="button"
        buttonStyle="Main"
        className={`min-w-[250px]
                    py-4
                    px-6
                    `}
        onClick={() => handleToggleDrawer()}
      >
        {isExtended ? 'Close order customization' : 'Customize Order'}
      </Button>
    </div>
  )
}
