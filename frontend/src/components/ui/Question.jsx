import React from 'react'

const Question = ({question}) => {
  return (
    <div className="flex items-start gap-3 justify-end">
        <div className="bg-custom/10 rounded-lg p-3 max-w-[80%]">
            <p className="text-gray-800">{question}</p>
        </div>
        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
            <i className="fas fa-user text-gray-600"></i>
        </div>
    </div>
  )
}

export default Question