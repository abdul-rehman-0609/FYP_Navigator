import { cn } from "@/lib/utils";

interface SkillBadgeProps {
  skill: string;
  proficiency?: "NOVICE" | "INTERMEDIATE" | "ADVANCED" | "EXPERT";
  size?: "sm" | "md";
  className?: string;
}

const proficiencyColors = {
  NOVICE: "bg-muted text-muted-foreground",
  INTERMEDIATE: "bg-teal/10 text-teal border-teal/20",
  ADVANCED: "bg-primary/10 text-primary border-primary/20",
  EXPERT: "bg-purple/10 text-purple border-purple/20",
};

export function SkillBadge({ skill, proficiency, size = "md", className }: SkillBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border font-medium transition-all",
        proficiency ? proficiencyColors[proficiency] : "bg-secondary text-secondary-foreground",
        size === "sm" ? "px-2 py-0.5 text-xs" : "px-3 py-1 text-sm",
        className
      )}
    >
      {skill}
      {proficiency && (
        <span className="ml-1.5 opacity-70 text-xs">
          {proficiency.charAt(0)}
        </span>
      )}
    </span>
  );
}
