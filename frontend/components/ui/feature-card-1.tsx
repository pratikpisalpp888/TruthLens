// components/ui/animated-feature-card.tsx

import * as React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils"; // Assuming you have a `cn` utility from shadcn

import { HTMLMotionProps } from "framer-motion";

// Define the props for the component
interface AnimatedFeatureCardProps extends Omit<HTMLMotionProps<"div">, "title"> {
  /** The numerical index to display, e.g., "001" */
  index: string;
  /** The tag or category label */
  tag: string;
  /** The main title or description */
  title: React.ReactNode;
  /** The React Node for the central icon */
  icon: React.ReactNode;
  /** The color variant which determines the gradient and tag color */
  color: "orange" | "purple" | "blue" | "teal" | "rose";
}

// Define HSL color values for each variant to work with shadcn's theming
const colorVariants = {
  orange: {
    '--feature-color': 'hsl(35, 91%, 55%)',
    '--feature-color-light': 'hsl(41, 100%, 85%)',
    '--feature-color-dark': 'hsl(24, 98%, 98%)',
  },
  purple: {
    '--feature-color': 'hsl(262, 85%, 60%)',
    '--feature-color-light': 'hsl(261, 100%, 87%)',
    '--feature-color-dark': 'hsl(264, 100%, 98%)',
  },
  blue: {
    '--feature-color': 'hsl(211, 100%, 60%)',
    '--feature-color-light': 'hsl(210, 100%, 83%)',
    '--feature-color-dark': 'hsl(216, 100%, 98%)',
  },
  teal: {
    '--feature-color': 'hsl(173, 80%, 40%)',
    '--feature-color-light': 'hsl(173, 80%, 85%)',
    '--feature-color-dark': 'hsl(173, 80%, 98%)',
  },
  rose: {
    '--feature-color': 'hsl(346, 87%, 60%)',
    '--feature-color-light': 'hsl(346, 100%, 85%)',
    '--feature-color-dark': 'hsl(346, 100%, 98%)',
  }
};

const AnimatedFeatureCard = React.forwardRef<
  HTMLDivElement,
  AnimatedFeatureCardProps
>(({ className, index, tag, title, icon, color, ...props }, ref) => {
  const cardStyle = colorVariants[color] as React.CSSProperties;

  return (
    <motion.div
      ref={ref}
      style={cardStyle}
      className={cn(
        "relative flex h-[350px] w-full max-w-sm flex-col justify-end overflow-hidden rounded-2xl border bg-white p-6 shadow-md transition-shadow hover:shadow-xl",
        className
      )}
      whileHover="hover"
      initial="initial"
      variants={{
        initial: { y: 0 },
        hover: { y: -10 },
      }}
      transition={{ type: "spring", stiffness: 200, damping: 15 }}
      {...props}
    >
      {/* Background Gradient */}
      <div
        className="absolute inset-0 z-0 opacity-40"
        style={{
          background: `radial-gradient(circle at 50% 40%, var(--feature-color-light) 0%, transparent 70%)`
        }}
      />
      
      {/* Index Number */}
      <div className="absolute top-6 left-6 font-mono text-lg font-bold text-slate-300">
        {index}
      </div>

      {/* Main Icon */}
      <motion.div 
        className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none"
        variants={{
            initial: { scale: 1, y: -20 },
            hover: { scale: 1.2, y: -40 },
        }}
        transition={{ type: "spring", stiffness: 200, damping: 15 }}
      >
        <div 
          className="w-32 h-32 rounded-full flex items-center justify-center bg-white shadow-[0_10px_30px_-10px_rgba(0,0,0,0.1)] border-[6px]"
          style={{ 
            borderColor: 'var(--feature-color-dark)', 
            color: 'var(--feature-color)',
            background: 'radial-gradient(circle, var(--feature-color-dark) 0%, white 100%)'
          }}
        >
          <div style={{ color: 'var(--feature-color)', filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.1))' }}>
            {icon}
          </div>
        </div>
      </motion.div>
      
      {/* Content */}
      <div className="relative z-20 rounded-xl border bg-white/95 p-5 backdrop-blur-sm shadow-sm flex flex-col items-start min-h-[140px] justify-center">
        <span
          className="mb-2 inline-block rounded-full px-3 py-1 text-[11px] font-bold uppercase tracking-wider shadow-sm"
          style={{ 
            backgroundColor: 'var(--feature-color-dark)', 
            color: 'var(--feature-color)' 
          }}
        >
          {tag}
        </span>
        <p className="text-sm font-medium text-slate-700 leading-relaxed">{title}</p>
      </div>
    </motion.div>
  );
});
AnimatedFeatureCard.displayName = "AnimatedFeatureCard";

export { AnimatedFeatureCard };
