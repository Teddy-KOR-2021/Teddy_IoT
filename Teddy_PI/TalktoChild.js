import React, { Component } from 'react';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import Stack from '@mui/material/Stack';
import TextareaAutosize from '@mui/material/TextareaAutosize';
import TeddyStore from '../Store/TeddyStore';


class TalktoChild extends Component {
    render() {
        const {goHome} = TeddyStore;
        return (
            <div>
                <br/><br/>
                <Stack
                direction="row"
                justifyContent="center"
                alignItems="center"
                spacing={2}
                >
                    <TextareaAutosize
                        aria-label="minimum height"
                        minRows={10}
                        placeholder="아이에게 하고 싶은 말을 입력하세요."
                        style={{ width: 300 }}
                    />
                </Stack>
                <p/>
                <Stack
                direction="row"
                justifyContent="center"
                alignItems="center"
                spacing={2}
                >
                    <Button variant="contained" endIcon={<SendIcon />}>
                        전송
                    </Button>
                    <Button onClick={()=>goHome()} variant="outlined" endIcon={<DeleteIcon />}>
                        취소
                    </Button>

                </Stack>
                
            </div>
        );
    }
}

export default TalktoChild;