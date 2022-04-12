import React from "react";
import ApplicationDropDown from "./elements/ApplicationDropDown";
import {Stack} from "@mui/material";


export default class ControlPanel extends React.Component {
    render() {
        return (
            <Stack spacing={2} sx={{ m: 2 }}>
                <ApplicationDropDown></ApplicationDropDown>
            </Stack>
            )
    }
}