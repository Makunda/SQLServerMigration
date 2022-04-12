import { configureStore } from '@reduxjs/toolkit'
import applicationReducer from './features/ApplicationSlice'

export default configureStore({
    reducer: {
        application: applicationReducer
    }
})