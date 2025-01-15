import { Box, Center, Container, IconButton, Input, Text, VStack, Textarea } from '@chakra-ui/react';
import {React, useEffect, useState } from 'react'
import { InputGroup } from '../components/ui/input-group';
import { IoIosSend } from "react-icons/io";
import { usePromptStore } from '../store/prompt';
import { PromptBox } from '../components/ui/PromptBox';

const HomePage = () => {
  const [newPrompt, setNewPrompt] = useState({query:""})
  const {prompts, createPrompt, fetchPrompts} = usePromptStore();
  const HandleAddPrompt = async() => {
    const {success, message} = await createPrompt(newPrompt);
    setNewPrompt({query:""});
  };
  useEffect(() => {
    fetchPrompts();
  },[fetchPrompts]);
  console.log("prompts: ", prompts);
  return (
    <Box minH="100%">
      <VStack spcing={8}>
        {prompts.map((prompt) => (
          <PromptBox key={prompt._id} prompt={prompt}/>
        ))}
      </VStack>
      <Box position={"fixed"} bottom={"0"} width={"full"}>
        <Center>
          <InputGroup width={"70%"} endElement={<IconButton size={"xs"} variant={"ghost"} onClick={HandleAddPrompt} _hover={{bg:'whiteAlpha.500'}}><IoIosSend/></IconButton>}>
            <Textarea overflow="hidden" autoresize placeholder={"message"} variant={"subtle"} value={newPrompt.query} onChange={ (e) => setNewPrompt({...newPrompt, query: e.target.value})}/>
          </InputGroup>          
        </Center>

      </Box>
    </Box>


  );
}

export default HomePage;