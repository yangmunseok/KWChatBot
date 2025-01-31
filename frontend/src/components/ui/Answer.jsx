import React from 'react'

const Answer = ({answer}) => {
  return (
    <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full bg-custom/10 flex items-center justify-center">
            <i className="fas fa-robot text-custom"></i>
        </div>
        <div className="bg-gray-100 rounded-lg p-3 max-w-[80%]">
            <p className="text-gray-800">{answer}</p>
        </div>
    </div>
  )
}

export default Answer