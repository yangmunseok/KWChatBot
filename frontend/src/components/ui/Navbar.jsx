import React, { useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query';
import logo from "@/assets/logo.png"

const Navbar = () => {
  const {data:authUser} = useQuery({queryKey:["authUser"]});
  const queryClient = useQueryClient();
  const buttonEventHandler = async(e) => {
    if(authUser) {
      await fetch("/api/auth/logout",{method:"POST"});
      queryClient.invalidateQueries({queryKey:["authUser"]});
    }
  }
  return (
  <header className="fixed top-0 left-0 right-0 bg-white/90 backdrop-blur-sm z-50 border-b border-gray-100">
    <nav className="max-w-8xl mx-auto px-6 h-20 flex items-center justify-between">
        <a href="/main" className="flex items-center">
            <img src={logo} alt="Logo" className="h-24"/>
        </a>
        <div className="hidden lg:flex items-center gap-x-8">
            <a href="/main" className="text-gray-600 hover:text-custom font-medium">Home</a>
            <a href="#" className="text-gray-600 hover:text-custom font-medium">Features</a>
            <a href="/chat" className="text-gray-600 hover:text-custom font-medium">Chat</a>
            <a href="#" className="text-gray-600 hover:text-custom font-medium">Contact</a>
            {authUser?
              <div className='relative'>
                <input type='checkbox' className='hidden peer' id='user-menu'/>
                <label htmlFor='user-menu'>
                  <img src="https://img.freepik.com/premium-vector/default-avatar-profile-icon-social-media-user-image-gray-avatar-icon-blank-profile-silhouette-vector-illustration_561158-3467.jpg?w=360" alt="User Profile" class="w-8 h-8 rounded-full"/>
                </label>
                <div class="absolute cursor-pointer right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg py-2 hidden peer-checked:block">
                  <button href="#" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 w-full text-start">Profile</button>
                  <a href="/setting">
                    <button href="#" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 w-full text-start">Settings</button>
                  </a>
                  
                  <button href="#" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 w-full text-start">Help</button>
                  <hr class="my-2 border-gray-200"/>
                  <button href="#" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 w-full text-start" onClick={buttonEventHandler}>Logout</button>
                </div>
              </div>
              : 
              <a href="/login">
                <button className="!rounded-button bg-custom text-white px-6 py-2.5 font-medium hover:bg-custom/90" onClick={buttonEventHandler}>
                  Login
                </button>
              </a>
              }       
        </div>


    </nav>
  </header>
  );
}

export default Navbar;
