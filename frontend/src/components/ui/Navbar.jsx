import { Container, HStack, IconButton, Flex, Button } from '@chakra-ui/react';
import React from 'react'
import {
  DrawerBackdrop,
  DrawerBody,
  DrawerCloseTrigger,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerRoot,
  DrawerTitle,
  DrawerTrigger,
} from "./drawer"
import {
  MenuContent,
  MenuItem,
  MenuRoot,
  MenuTrigger,
} from "./menu"
import { Avatar, AvatarGroup } from "./avatar"
import { IoIosMenu } from "react-icons/io";
import { IoChatboxEllipses } from "react-icons/io5";
const Navbar = () => {
  return (
    <Container maxW={"1140px"} px={"4"}>
        <Flex
            h={16}
            alignItems={"center"}
            justifyContent={"space-between"}
            flexDir={{
                base:"column",
                sm:"row",
            }}
        >
          <HStack spacing={2} alignItems={"center"}>
            <DrawerRoot size={"sm"} placement={"start"}>
              <DrawerBackdrop />
              <DrawerTrigger asChild>
                <IconButton variant={"ghost"}>
                  <IoIosMenu/>
                </IconButton>
              </DrawerTrigger>
              <DrawerContent>
                <DrawerHeader>
                  <DrawerTitle>
                    Side Menu
                  </DrawerTitle>
                </DrawerHeader>
                <DrawerBody>
                  <p>
                    chat list
                  </p>
                </DrawerBody>
                <DrawerFooter>close</DrawerFooter>
                <DrawerCloseTrigger />
              </DrawerContent>
            </DrawerRoot>
            <IconButton variant={"ghost"}>
              <IoChatboxEllipses />
            </IconButton>
            <MenuRoot>
              <MenuTrigger asChild>
                <Button variant={"ghost"}>
                  ChatGpt
                </Button>
              </MenuTrigger>
              <MenuContent>
                <MenuItem value="LLaMa 3">
                  LLaMa 3
                </MenuItem>
                <MenuItem value="Falcon 2">
                  Falcon 2
                </MenuItem>
                <MenuItem value="Gemma">
                  Gemma
                </MenuItem>
              </MenuContent>
            </MenuRoot>
          </HStack>
          <Avatar src="https://bit.ly/broken-link" colorPalette="red"/>
        </Flex>      

    </Container>
  );
}

export default Navbar;