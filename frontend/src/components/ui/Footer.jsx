import React from 'react'

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-16">
        <div className="max-w-8xl mx-auto px-6">
            <div className="grid md:grid-cols-3 gap-12">
                <div className="space-y-6">
                    <h4 className="text-lg font-semibold">KW</h4>
                    <p className="text-gray-400">Redefining Communication with AI.</p>
                </div>
                <div className="space-y-6">
                    <h4 className="text-lg font-semibold">Quick Links</h4>
                    <ul className="space-y-4">
                        <li><a href="#" className="text-gray-400 hover:text-white">About Us</a></li>
                        <li><a href="#" className="text-gray-400 hover:text-white">Features</a></li>
                        <li><a href="#" className="text-gray-400 hover:text-white">Pricing</a></li>
                        <li><a href="#" className="text-gray-400 hover:text-white">Contact</a></li>
                    </ul>
                </div>
                <div className="space-y-6">
                    <h4 className="text-lg font-semibold">Connect With Us</h4>
                    <div className="flex space-x-4">
                        <a href="#" className="text-gray-400 hover:text-white text-xl"><i className="fab fa-twitter"></i></a>
                        <a href="#" className="text-gray-400 hover:text-white text-xl"><i className="fab fa-linkedin"></i></a>
                        <a href="#" className="text-gray-400 hover:text-white text-xl"><i className="fab fa-facebook"></i></a>
                        <a href="#" className="text-gray-400 hover:text-white text-xl"><i className="fab fa-instagram"></i></a>
                    </div>
                </div>
            </div>
        </div>
    </footer>
  )
}

export default Footer