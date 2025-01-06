import { Box, Center, Container, IconButton, Input, Text, VStack, Textarea } from '@chakra-ui/react';
import {React, useState } from 'react'
import { InputGroup } from '../components/ui/input-group';
import { IoIosSend } from "react-icons/io";
import { usePromptStore } from '../store/prompt';

const HomePage = () => {
  const [newPrompt, setNewPrompt] = useState({query:""})
  const {prompts, createPrompt} = usePromptStore();
  const HandleAddPrompt = async() => {
    const {success, message} = await createPrompt(newPrompt);
    setNewPrompt({query:""});
  };
  return (
    <Box minH="100%">
      <VStack spcing={8}>
        {prompts.map((prompt,index) => (
          <Text key={index}>{prompt}</Text>
        ))}
      </VStack>

      <Box position={"fixed"} bottom={"0"} width={"full"}>
        <Center>
          <InputGroup width={"70%"} endElement={<IconButton size={"xs"} variant={"plain"} onClick={HandleAddPrompt}><IoIosSend/></IconButton>}>
            <Textarea overflow="hidden" autoresize placeholder={"message"} variant={"subtle"} value={newPrompt.query} onChange={ (e) => setNewPrompt({...newPrompt, query: e.target.value})}/>
          </InputGroup>          
        </Center>

      </Box>
    </Box>


  );
}

export default HomePage;