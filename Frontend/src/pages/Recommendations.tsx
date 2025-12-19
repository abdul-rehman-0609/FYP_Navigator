import { useState, useEffect } from "react";
import { Lightbulb, Loader2, Save, Sparkles, BookOpen, Code, Check, AlertTriangle, ShieldAlert } from "lucide-react";
import { Layout } from "@/components/layout/Layout";
import { PageHeader } from "@/components/ui/page-header";
import { EmptyState } from "@/components/ui/empty-state";
import { MatchScore } from "@/components/ui/match-score";
import { SkillBadge } from "@/components/ui/skill-badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { api, Student, Recommendation } from "@/lib/api";
import { toast } from "sonner";

export default function Recommendations() {
  const [students, setStudents] = useState<Student[]>([]);
  const [selectedStudent, setSelectedStudent] = useState<string>("");
  const [count, setCount] = useState(5);
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [saving, setSaving] = useState(false);
  const [selecting, setSelecting] = useState<string | null>(null);

  useEffect(() => {
    api.getStudents()
      .then(setStudents)
      .catch(() => {
        // Fallback for demo/testing if server offline
        setStudents([
          { id: "STU001", name: "Ahmad Khan", cgpa: 3.5, major: "CS", year: 4, skills: [], interests: [], completed_courses: [], preferences: { max_weekly_hours: 20, team_size: 2, preferred_domains: [] } },
          { id: "STU002", name: "Sara Ahmed", cgpa: 3.8, major: "SE", year: 4, skills: [], interests: [], completed_courses: [], preferences: { max_weekly_hours: 25, team_size: 3, preferred_domains: [] } },
        ]);
      });
  }, []);

  const generate = async () => {
    if (!selectedStudent) {
      toast.error("Please select a student");
      return;
    }
    setLoading(true);
    setRecommendations([]); // Clear previous results
    try {
      const data = await api.getRecommendations(selectedStudent, count);
      setRecommendations(data);
      toast.success(`Generated ${data.length} recommendations`);
    } catch (error) {
      toast.error("Failed to generate recommendations");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const saveToHistory = async () => {
    if (!selectedStudent || recommendations.length === 0) return;
    setSaving(true);
    try {
      await api.saveToHistory(selectedStudent, recommendations);
      toast.success("Saved to history");
    } catch {
      toast.error("Failed to save history");
    } finally {
      setSaving(false);
    }
  };

  const handleSelectTopic = async (topicId: string, score: number) => {
    if (!selectedStudent) return;
    setSelecting(topicId);
    try {
      await api.selectTopic(selectedStudent, topicId, score);
      toast.success("Topic selected successfully!");
    } catch (error: any) {
      toast.error(error.message || "Failed to select topic");
    } finally {
      setSelecting(null);
    }
  };

  const selectedStudentData = students.find((s) => s.id === selectedStudent);

  const getRiskColor = (level: string) => {
    const l = level?.toLowerCase();
    if (l?.includes("low")) return "bg-emerald/10 text-emerald";
    if (l?.includes("medium")) return "bg-amber/10 text-amber";
    return "bg-destructive/10 text-destructive";
  };

  return (
    <Layout>
      <PageHeader
        title="Recommendations"
        description="Generate personalized FYP topic recommendations"
      />

      {/* Controls */}
      <Card className="mb-8 max-w-2xl">
        <CardContent className="pt-6 space-y-6">
          <div className="space-y-2">
            <Label>Select Student</Label>
            <Select value={selectedStudent} onValueChange={setSelectedStudent}>
              <SelectTrigger>
                <SelectValue placeholder="Choose a student..." />
              </SelectTrigger>
              <SelectContent>
                {students.map((s) => (
                  <SelectItem key={s.id} value={s.id}>
                    {s.name} ({s.id})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Number of Recommendations: {count}</Label>
            <Slider
              value={[count]}
              onValueChange={([v]) => setCount(v)}
              min={1}
              max={10}
              step={1}
            />
          </div>

          <Button onClick={generate} disabled={loading || !selectedStudent} className="w-full gap-2">
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Sparkles className="h-4 w-4" />
            )}
            Generate Recommendations
          </Button>
        </CardContent>
      </Card>

      {/* Results */}
      {recommendations.length > 0 ? (
        <>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-display font-semibold">
              Results for {selectedStudentData?.name}
            </h2>
            <Button variant="outline" onClick={saveToHistory} disabled={saving}>
              {saving ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Save className="h-4 w-4 mr-2" />
              )}
              Save to History
            </Button>
          </div>

          <div className="space-y-4">
            {recommendations.map((rec, idx) => (
              <Card
                key={rec.topic_id}
                className="overflow-hidden animate-fade-in hover:shadow-lg transition-shadow"
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <CardHeader className="pb-4">
                  <div className="flex items-start gap-4">
                    <MatchScore score={rec.match_score} size="md" />
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded-full">
                          {rec.domain}
                        </span>
                        {rec.risk_level && (
                          <span className={`text-xs px-2 py-0.5 rounded-full flex items-center gap-1 ${getRiskColor(rec.risk_level)}`}>
                            {rec.risk_level.toLowerCase().includes("high") ? <AlertTriangle className="h-3 w-3" /> : <ShieldAlert className="h-3 w-3" />}
                            Risk: {rec.risk_level}
                          </span>
                        )}
                      </div>
                      <CardTitle className="text-lg">{rec.title}</CardTitle>
                      <p className="text-muted-foreground mt-2 text-sm">
                        {rec.description}
                      </p>
                    </div>
                    <Button 
                      size="sm" 
                      onClick={() => handleSelectTopic(rec.topic_id, rec.match_score)}
                      disabled={selecting === rec.topic_id}
                      variant="default"
                    >
                      {selecting === rec.topic_id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Check className="h-4 w-4 mr-1" />}
                      Select Topic
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <Accordion type="single" collapsible>
                    <AccordionItem value="details" className="border-none">
                      <AccordionTrigger className="py-2 text-sm">
                        View Details
                      </AccordionTrigger>
                      <AccordionContent>
                        <div className="space-y-4 pt-2">
                          {/* Technical Feasibility */}
                          {rec.feasibility_score !== undefined && (
                            <div className="space-y-1">
                               <div className="flex justify-between text-sm">
                                 <span className="font-medium text-muted-foreground">Technical Feasibility</span>
                                 <span className="font-bold">{(rec.feasibility_score * 100).toFixed(0)}%</span>
                               </div>
                               <div className="h-2 bg-secondary rounded-full overflow-hidden">
                                 <div 
                                   className="h-full bg-blue-500 rounded-full" 
                                   style={{ width: `${rec.feasibility_score * 100}%` }}
                                 />
                               </div>
                            </div>
                          )}

                          {/* Explanation / Match Reasons */}
                          <div className="p-4 bg-emerald/5 border border-emerald/20 rounded-lg">
                            <div className="flex items-center gap-2 text-emerald font-medium mb-2">
                              <Lightbulb className="h-4 w-4" />
                              Why this matches
                            </div>
                            <p className="text-sm text-muted-foreground mb-2">
                              {rec.explanation}
                            </p>
                            {rec.match_reasons && rec.match_reasons.length > 0 && (
                              <ul className="list-disc list-inside text-sm text-emerald-700/80 space-y-1">
                                {rec.match_reasons.map((reason, i) => (
                                  <li key={i}>{reason}</li>
                                ))}
                              </ul>
                            )}
                          </div>

                          {/* Risk Reasons */}
                          {rec.risk_reasons && rec.risk_reasons.length > 0 && (
                             <div className="p-4 bg-red-50 border border-red-100 rounded-lg">
                               <div className="flex items-center gap-2 text-red-600 font-medium mb-2">
                                 <AlertTriangle className="h-4 w-4" />
                                 Potential Risks / Gaps
                               </div>
                               <ul className="list-disc list-inside text-sm text-red-600/80 space-y-1">
                                 {rec.risk_reasons.map((reason, i) => (
                                   <li key={i}>{reason}</li>
                                 ))}
                               </ul>
                             </div>
                          )}

                          {/* Required Skills */}
                          <div>
                            <div className="flex items-center gap-2 mb-2">
                              <Code className="h-4 w-4 text-primary" />
                              <span className="text-sm font-medium">Required Skills</span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                              {rec.required_skills.map((skill) => (
                                <SkillBadge key={skill} skill={skill} size="sm" />
                              ))}
                            </div>
                          </div>

                          {/* Required Courses */}
                          <div>
                            <div className="flex items-center gap-2 mb-2">
                              <BookOpen className="h-4 w-4 text-teal" />
                              <span className="text-sm font-medium">Required Courses</span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                              {rec.required_courses.map((course) => (
                                <span
                                  key={course}
                                  className="px-2 py-1 bg-teal/10 text-teal text-xs rounded-full"
                                >
                                  {course}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </AccordionContent>
                    </AccordionItem>
                  </Accordion>
                </CardContent>
              </Card>
            ))}
          </div>
        </>
      ) : (
        !loading && (
          <EmptyState
            icon={Lightbulb}
            title="No recommendations yet"
            description="Select a student and generate recommendations to see results"
          />
        )
      )}
    </Layout>
  );
}
