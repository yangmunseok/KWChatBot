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
  <header className="fixed top-0 left-0 right-0 bg-white/90 backdrop-blur-sm z-50 border-b border-gray-100">
    <nav className="max-w-8xl mx-auto px-6 h-20 flex items-center justify-between">
        <a href="#" className="flex items-center">
            <img src="../src/assets/logo.png" alt="Logo" class="h-24"/>
        </a>
        <div className="hidden lg:flex items-center space-x-8">
            <a href="#" className="text-custom font-medium">Home</a>
            <a href="#" className="text-gray-600 hover:text-custom font-medium">Features</a>
            <a href="#" className="text-gray-600 hover:text-custom font-medium">Pricing</a>
            <a href="#" className="text-gray-600 hover:text-custom font-medium">Contact</a>
            <a href="http://localhost:5173/login">
              <button className="!rounded-button bg-custom text-white px-6 py-2.5 font-medium hover:bg-custom/90">Get Started</button>
            </a>
            
        </div>
    </nav>
  </header>
  );
}

export default Navbar;