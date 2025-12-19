import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  color?: "blue" | "coral" | "teal" | "purple" | "amber";
  className?: string;
}

const colorClasses = {
  blue: "bg-primary/10 text-primary",
  coral: "bg-coral/10 text-coral",
  teal: "bg-teal/10 text-teal",
  purple: "bg-purple/10 text-purple",
  amber: "bg-amber/10 text-amber",
};

export function StatCard({ title, value, icon: Icon, trend, color = "blue", className }: StatCardProps) {
  return (
    <div className={cn(
      "bg-card rounded-2xl p-6 shadow-sm border border-border/50 hover:shadow-md transition-all duration-300 animate-fade-in",
      className
    )}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-muted-foreground font-medium">{title}</p>
          <p className="text-3xl font-display font-bold mt-1">{value}</p>
          {trend && (
            <p className="text-xs text-emerald mt-2">{trend}</p>
          )}
        </div>
        <div className={cn("p-3 rounded-xl", colorClasses[color])}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  );
}
