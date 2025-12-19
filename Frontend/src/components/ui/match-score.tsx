import { cn } from "@/lib/utils";

interface MatchScoreProps {
  score: number;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function MatchScore({ score, size = "md", className }: MatchScoreProps) {
  const percentage = Math.round(score * 100);
  const circumference = 2 * Math.PI * 40;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const sizeClasses = {
    sm: "w-12 h-12",
    md: "w-20 h-20",
    lg: "w-24 h-24",
  };

  const textSizes = {
    sm: "text-xs",
    md: "text-lg",
    lg: "text-xl",
  };

  const getColor = () => {
    if (percentage >= 80) return "text-emerald";
    if (percentage >= 60) return "text-teal";
    if (percentage >= 40) return "text-amber";
    return "text-coral";
  };

  return (
    <div className={cn("relative", sizeClasses[size], className)}>
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
        <circle
          cx="50"
          cy="50"
          r="40"
          fill="none"
          stroke="currentColor"
          strokeWidth="8"
          className="text-muted"
        />
        <circle
          cx="50"
          cy="50"
          r="40"
          fill="none"
          stroke="currentColor"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          className={cn("transition-all duration-1000 ease-out", getColor())}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className={cn("font-display font-bold", textSizes[size])}>
          {percentage}%
        </span>
      </div>
    </div>
  );
}
