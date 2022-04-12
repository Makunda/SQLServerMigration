import {createSlice, PayloadAction} from '@reduxjs/toolkit'

export const applicationSlice = createSlice({
    name: 'application',
    initialState: {
        applicationName: ""
    },
    reducers: {
        changeApplication: (state, action:PayloadAction<string>) => {
            state.applicationName = action.payload
        }
    }
})

// Action creators are generated for each case reducer function
export const { changeApplication } = applicationSlice.actions

export default applicationSlice.reducer