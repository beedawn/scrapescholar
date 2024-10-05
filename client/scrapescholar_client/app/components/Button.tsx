import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  type?: any;
}

const Button: React.FC<ButtonProps> = ({ 
  children, onClick, className, type = 'button' 
}) => {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 bg-blue-500 
        text-white rounded ${className}`}
      type={type}
    >
      {children}
    </button>
  );
};

export default Button;
