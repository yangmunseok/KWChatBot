import React from 'react'
import { useCookieStore } from '../store/cookie'
import { useState } from 'react';
import { Box, Button, Input, VStack } from '@chakra-ui/react';

const TestPage = () => {
    const [user,setUser] = useState({userId:"",userPwd:""});
    const {getCookies} = useCookieStore();

    const handleLogin = async() => {
        await getCookies(user);
        console.log("nice!");
    }
  return (
    <Box w={"full"} bg={"gray.800"} p={6} rounded={"lg"} shadow={"md"}>
        <VStack spacing={4}>
            <Input
                placeholder='id'
                name='id'
                value={user.userId}
                onChange={(e) => setUser({ ...user, userId: e.target.value })}
            />
            <Input
                placeholder='password'
                name='password'
                value={user.userPwd}
                onChange={(e) => setUser({ ...user, userPwd: e.target.value })}
            />
            <Button colorScheme='blue' onClick={handleLogin} w='full'>
                Add Product
            </Button>
        </VStack>
    </Box>
  )
}

export default TestPage