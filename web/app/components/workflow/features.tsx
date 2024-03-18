import {
  memo,
  useCallback,
} from 'react'
import { useTranslation } from 'react-i18next'
import { useStore } from './store'
import {
  useIsChatMode,
  useNodesSyncDraft,
} from './hooks'
import { XClose } from '@/app/components/base/icons/src/vender/line/general'
import {
  FeaturesChoose,
  FeaturesPanel,
} from '@/app/components/base/features'

const Features = () => {
  const { t } = useTranslation()
  const isChatMode = useIsChatMode()
  const setShowFeaturesPanel = useStore(state => state.setShowFeaturesPanel)
  const { handleSyncWorkflowDraft } = useNodesSyncDraft()

  const handleFeaturesChange = useCallback(() => {
    handleSyncWorkflowDraft()
  }, [handleSyncWorkflowDraft])

  return (
    <div className='fixed top-16 left-2 bottom-2 w-[600px] rounded-2xl border-[0.5px] border-gray-200 bg-white shadow-xl z-10'>
      <div className='flex items-center justify-between px-4 pt-3'>
        {t('workflow.common.features')}
        <div className='flex items-center'>
          {
            isChatMode && (
              <>
                <FeaturesChoose onChange={handleFeaturesChange} />
                <div className='mx-3 w-[1px] h-[14px] bg-gray-200'></div>
              </>
            )
          }
          <div
            className='flex items-center justify-center w-6 h-6 cursor-pointer'
            onClick={() => setShowFeaturesPanel(false)}
          >
            <XClose className='w-4 h-4 text-gray-500' />
          </div>
        </div>
      </div>
      <div className='p-4'>
        <FeaturesPanel
          onChange={handleFeaturesChange}
          openingStatementProps={{
            onAutoAddPromptVariable: () => {},
          }}
        />
      </div>
    </div>
  )
}

export default memo(Features)
