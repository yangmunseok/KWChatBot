import { Box, Container, Flex, HStack, Image } from '@chakra-ui/react';
import React from 'react'

export const PromptBox = ({prompt}) => {
  return (
    <Box maxW={"1140px"} px={"4"} borderSpacing={"5px"}>

        <Box 
            display={"flex"}
            maxWidth={"50%"} 
            justifySelf={"flex-end"} 
            margin={"0px"} 
            borderRadius={"10px"}
            padding={"10px"}
            backgroundColor={"gray.800"}
            position={"relative"}
            _after={{
                content: '""',
                position: "absolute",
                bottom: "50%", // 꼬리의 위치
                left: "100%",    // 꼬리의 좌우 위치
                borderWidth: "10px", // 삼각형 크기
                borderStyle: "solid",
                borderColor:"transparent",
                borderLeftColor:"gray.800",
                transform: "translateY(50%)"
            }}
        >
            {prompt.question}
        </Box>
        <HStack>
            <Image src="https://news.kw.ac.kr/mascot/img/uni_02.png"/>
            <Box 
                margin={"10px"} 
                padding={"50px"}
                backgroundColor={"gray.600"}
                borderRadius={"10px"}
                position={"relative"}
                _after={{
                    content: '""',
                    position: "absolute",
                    bottom: "50%", // 꼬리의 위치
                    right: "100%",    // 꼬리의 좌우 위치
                    borderWidth: "10px", // 삼각형 크기
                    borderStyle: "solid",
                    borderColor:"transparent",
                    borderRightColor:"gray.600",
                    transform: "translateY(50%)"
                }}
            >
                {prompt.answer}
            </Box>            
        </HStack>

    </Box>

  );
}
