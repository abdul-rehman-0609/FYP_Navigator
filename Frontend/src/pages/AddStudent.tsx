import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { ChevronLeft, ChevronRight, Plus, X, Save, Loader2 } from "lucide-react";
import { Layout } from "@/components/layout/Layout";
import { PageHeader } from "@/components/ui/page-header";
import { SkillBadge } from "@/components/ui/skill-badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { api, Student, Skill, Interest, DropdownOptions } from "@/lib/api";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

const defaultOptions: DropdownOptions = {
  skills: ["Python", "Java", "JavaScript", "C++", "Machine Learning", "Deep Learning", "NLP", "React", "Node.js", "Docker", "AWS", "SQL", "MongoDB", "Git", "TensorFlow", "PyTorch", "OpenCV", "Unity", "Blockchain", "Flutter"],
  courses: ["Artificial Intelligence", "Computer Graphics", "Computer Networks", "Data Structures", "Database Systems", "Distributed Systems", "Embedded Systems", "Ethics in Computing", "Information Security", "Linear Algebra", "Mobile Application Development", "Statistics", "Web Engineering"],
  domains: ["Artificial Intelligence", "Cloud Computing", "Cybersecurity", "Data Science", "Game Development", "IoT", "Mobile Development", "Web Development"],
  majors: ["Computer Science", "Software Engineering", "Information Technology", "Data Science", "Cybersecurity"],
  proficiency_levels: ["NOVICE", "INTERMEDIATE", "ADVANCED", "EXPERT"],
  interest_levels: ["LOW", "MEDIUM", "HIGH", "VERY_HIGH"],
};

const steps = ["Basic Info", "Skills", "Interests", "Courses", "Preferences"];

export default function AddStudent() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const editId = searchParams.get("edit");

  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [options, setOptions] = useState<DropdownOptions>(defaultOptions);

  const [formData, setFormData] = useState({
    id: "",
    name: "",
    cgpa: 3.0,
    major: "",
    year: 4,
  });

  const [skills, setSkills] = useState<Skill[]>([]);
  const [newSkill, setNewSkill] = useState({ name: "", proficiency: "INTERMEDIATE" as const });

  const [interests, setInterests] = useState<Interest[]>([]);
  const [newInterest, setNewInterest] = useState({ domain: "", level: "MEDIUM" as const });

  const [courses, setCourses] = useState<string[]>([]);
  const [preferences, setPreferences] = useState({
    max_weekly_hours: 20,
    team_size: 2,
    preferred_domains: [] as string[],
  });

  useEffect(() => {
    api.getOptions().then(setOptions).catch(() => {});
    if (editId) {
      api.getStudent(editId).then((student) => {
        setFormData({
          id: student.id,
          name: student.name,
          cgpa: student.cgpa,
          major: student.major,
          year: student.year,
        });
        setSkills(student.skills);
        setInterests(student.interests);
        setCourses(student.completed_courses);
        setPreferences(student.preferences);
      }).catch(() => toast.error("Failed to load student"));
    }
  }, [editId]);

  const addSkill = () => {
    if (!newSkill.name) return;
    if (skills.find((s) => s.name === newSkill.name)) {
      toast.error("Skill already added");
      return;
    }
    setSkills([...skills, newSkill]);
    setNewSkill({ name: "", proficiency: "INTERMEDIATE" });
  };

  const addInterest = () => {
    if (!newInterest.domain) return;
    if (interests.find((i) => i.domain === newInterest.domain)) {
      toast.error("Interest already added");
      return;
    }
    setInterests([...interests, newInterest]);
    setNewInterest({ domain: "", level: "MEDIUM" });
  };

  const toggleCourse = (course: string) => {
    setCourses((prev) =>
      prev.includes(course) ? prev.filter((c) => c !== course) : [...prev, course]
    );
  };

  const toggleDomain = (domain: string) => {
    setPreferences((prev) => ({
      ...prev,
      preferred_domains: prev.preferred_domains.includes(domain)
        ? prev.preferred_domains.filter((d) => d !== domain)
        : [...prev.preferred_domains, domain],
    }));
  };

  const handleSubmit = async () => {
    if (!formData.id || !formData.name || !formData.major) {
      toast.error("Please fill in all required fields");
      setStep(0);
      return;
    }

    setLoading(true);
    try {
      const student: Omit<Student, "id"> & { id?: string } = {
        ...formData,
        skills,
        interests,
        completed_courses: courses,
        preferences,
      };

      if (editId) {
        await api.updateStudent(editId, student);
        toast.success("Student updated successfully");
      } else {
        await api.createStudent(student as Student);
        toast.success("Student added successfully");
      }
      navigate("/students");
    } catch {
      toast.error("Failed to save student");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <PageHeader
        title={editId ? "Edit Student" : "Add New Student"}
        description="Create a comprehensive student profile"
      />

      {/* Progress Steps */}
      <div className="flex items-center justify-between mb-8 max-w-3xl">
        {steps.map((s, idx) => (
          <button
            key={s}
            onClick={() => setStep(idx)}
            className={cn(
              "flex items-center gap-2 transition-all",
              idx <= step ? "text-primary" : "text-muted-foreground"
            )}
          >
            <div
              className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all",
                idx < step
                  ? "bg-primary text-primary-foreground"
                  : idx === step
                  ? "bg-primary text-primary-foreground ring-4 ring-primary/20"
                  : "bg-muted text-muted-foreground"
              )}
            >
              {idx + 1}
            </div>
            <span className="hidden sm:block text-sm font-medium">{s}</span>
          </button>
        ))}
      </div>

      <Card className="max-w-3xl animate-fade-in">
        <CardHeader>
          <CardTitle>{steps[step]}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Step 1: Basic Info */}
          {step === 0 && (
            <>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="id">Student ID *</Label>
                  <Input
                    id="id"
                    placeholder="e.g., STU001"
                    value={formData.id}
                    onChange={(e) => setFormData({ ...formData, id: e.target.value })}
                    disabled={!!editId}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name *</Label>
                  <Input
                    id="name"
                    placeholder="e.g., Ahmad Khan"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label>Major *</Label>
                  <Select
                    value={formData.major}
                    onValueChange={(v) => setFormData({ ...formData, major: v })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select major" />
                    </SelectTrigger>
                    <SelectContent>
                      {options.majors.map((m) => (
                        <SelectItem key={m} value={m}>
                          {m}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>Year</Label>
                  <Select
                    value={String(formData.year)}
                    onValueChange={(v) => setFormData({ ...formData, year: Number(v) })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {[1, 2, 3, 4, 5].map((y) => (
                        <SelectItem key={y} value={String(y)}>
                          Year {y}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>CGPA: {formData.cgpa.toFixed(2)}</Label>
                  <Slider
                    value={[formData.cgpa]}
                    onValueChange={([v]) => setFormData({ ...formData, cgpa: v })}
                    min={0}
                    max={4}
                    step={0.1}
                    className="mt-3"
                  />
                </div>
              </div>
            </>
          )}

          {/* Step 2: Skills */}
          {step === 1 && (
            <>
              <div className="flex gap-3">
                <Select
                  value={newSkill.name}
                  onValueChange={(v) => setNewSkill({ ...newSkill, name: v })}
                >
                  <SelectTrigger className="flex-1">
                    <SelectValue placeholder="Select a skill" />
                  </SelectTrigger>
                  <SelectContent>
                    {options.skills.map((s) => (
                      <SelectItem key={s} value={s}>
                        {s}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select
                  value={newSkill.proficiency}
                  onValueChange={(v: any) => setNewSkill({ ...newSkill, proficiency: v })}
                >
                  <SelectTrigger className="w-40">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {options.proficiency_levels.map((p) => (
                      <SelectItem key={p} value={p}>
                        {p}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Button onClick={addSkill} size="icon">
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex flex-wrap gap-2 min-h-[100px] p-4 bg-muted/50 rounded-lg">
                {skills.length === 0 ? (
                  <p className="text-muted-foreground text-sm">No skills added yet</p>
                ) : (
                  skills.map((skill) => (
                    <div key={skill.name} className="flex items-center gap-1 animate-scale-in">
                      <SkillBadge skill={skill.name} proficiency={skill.proficiency} />
                      <button
                        onClick={() => setSkills(skills.filter((s) => s.name !== skill.name))}
                        className="text-muted-foreground hover:text-destructive"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </>
          )}

          {/* Step 3: Interests */}
          {step === 2 && (
            <>
              <div className="flex gap-3">
                <Select
                  value={newInterest.domain}
                  onValueChange={(v) => setNewInterest({ ...newInterest, domain: v })}
                >
                  <SelectTrigger className="flex-1">
                    <SelectValue placeholder="Select a domain" />
                  </SelectTrigger>
                  <SelectContent>
                    {options.domains.map((d) => (
                      <SelectItem key={d} value={d}>
                        {d}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select
                  value={newInterest.level}
                  onValueChange={(v: any) => setNewInterest({ ...newInterest, level: v })}
                >
                  <SelectTrigger className="w-36">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {options.interest_levels.map((l) => (
                      <SelectItem key={l} value={l}>
                        {l}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Button onClick={addInterest} size="icon">
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex flex-wrap gap-2 min-h-[100px] p-4 bg-muted/50 rounded-lg">
                {interests.length === 0 ? (
                  <p className="text-muted-foreground text-sm">No interests added yet</p>
                ) : (
                  interests.map((interest) => (
                    <div
                      key={interest.domain}
                      className="flex items-center gap-1 px-3 py-1.5 bg-purple/10 text-purple rounded-full animate-scale-in"
                    >
                      <span className="text-sm font-medium">
                        {interest.domain} ({interest.level})
                      </span>
                      <button
                        onClick={() =>
                          setInterests(interests.filter((i) => i.domain !== interest.domain))
                        }
                        className="hover:text-destructive"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </>
          )}

          {/* Step 4: Courses */}
          {step === 3 && (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {options.courses.map((course) => (
                <button
                  key={course}
                  onClick={() => toggleCourse(course)}
                  className={cn(
                    "p-3 rounded-lg text-sm font-medium text-left transition-all",
                    courses.includes(course)
                      ? "bg-teal/10 text-teal border-2 border-teal"
                      : "bg-muted/50 hover:bg-muted border-2 border-transparent"
                  )}
                >
                  {course}
                </button>
              ))}
            </div>
          )}

          {/* Step 5: Preferences */}
          {step === 4 && (
            <>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label>Max Weekly Hours: {preferences.max_weekly_hours}h</Label>
                  <Slider
                    value={[preferences.max_weekly_hours]}
                    onValueChange={([v]) =>
                      setPreferences({ ...preferences, max_weekly_hours: v })
                    }
                    min={5}
                    max={40}
                    step={5}
                  />
                </div>
                <div className="space-y-2">
                  <Label>Preferred Team Size: {preferences.team_size}</Label>
                  <Slider
                    value={[preferences.team_size]}
                    onValueChange={([v]) => setPreferences({ ...preferences, team_size: v })}
                    min={1}
                    max={5}
                    step={1}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Preferred Domains</Label>
                <div className="flex flex-wrap gap-2">
                  {options.domains.map((domain) => (
                    <button
                      key={domain}
                      onClick={() => toggleDomain(domain)}
                      className={cn(
                        "px-3 py-1.5 rounded-full text-sm font-medium transition-all",
                        preferences.preferred_domains.includes(domain)
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted hover:bg-muted/80"
                      )}
                    >
                      {domain}
                    </button>
                  ))}
                </div>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between max-w-3xl mt-6">
        <Button
          variant="outline"
          onClick={() => setStep(Math.max(0, step - 1))}
          disabled={step === 0}
        >
          <ChevronLeft className="h-4 w-4 mr-1" />
          Previous
        </Button>
        {step < steps.length - 1 ? (
          <Button onClick={() => setStep(step + 1)}>
            Next
            <ChevronRight className="h-4 w-4 ml-1" />
          </Button>
        ) : (
          <Button onClick={handleSubmit} disabled={loading}>
            {loading ? (
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <Save className="h-4 w-4 mr-2" />
            )}
            {editId ? "Update" : "Save"} Student
          </Button>
        )}
      </div>
    </Layout>
  );
}
