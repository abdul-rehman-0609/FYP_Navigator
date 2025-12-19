import { useState, useEffect } from "react";
import { History as HistoryIcon, Calendar, User, Trash2, FileDown } from "lucide-react";
import { Layout } from "@/components/layout/Layout";
import { PageHeader } from "@/components/ui/page-header";
import { EmptyState } from "@/components/ui/empty-state";
import { MatchScore } from "@/components/ui/match-score";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { api, HistoryEntry, Student } from "@/lib/api";
import { toast } from "sonner";

export default function History() {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [filter, setFilter] = useState<string>("all");
  const [loading, setLoading] = useState(true);
  const [clearOpen, setClearOpen] = useState(false);

  useEffect(() => {
    Promise.all([
      api.getHistory().catch(() => []),
      api.getStudents().catch(() => []),
    ]).then(([h, s]) => {
      setHistory(h.length ? h : mockHistory);
      setStudents(s);
      setLoading(false);
    });
  }, []);

  const mockHistory: HistoryEntry[] = [
    {
      id: "H001",
      student_id: "STU001",
      student_name: "Ahmad Khan",
      timestamp: new Date().toISOString(),
      recommendations: [
        {
          topic_id: "T001",
          title: "AI-Powered Student Performance Predictor",
          description: "ML system for predicting academic performance",
          match_score: 0.92,
          required_skills: ["Python", "ML"],
          required_courses: ["AI"],
          explanation: "Great match for your skills",
          domain: "AI",
        },
      ],
    },
    {
      id: "H002",
      student_id: "STU002",
      student_name: "Sara Ahmed",
      timestamp: new Date(Date.now() - 86400000).toISOString(),
      recommendations: [
        {
          topic_id: "T002",
          title: "E-Commerce Platform with AI Chatbot",
          description: "Web platform with intelligent customer service",
          match_score: 0.88,
          required_skills: ["JavaScript", "React"],
          required_courses: ["Web Engineering"],
          explanation: "Matches your web development expertise",
          domain: "Web Development",
        },
      ],
    },
  ];

  const filtered = filter === "all" ? history : history.filter((h) => h.student_id === filter);

  const handleClear = async () => {
    try {
      await api.clearHistory();
      setHistory([]);
      toast.success("History cleared");
    } catch {
      setHistory([]);
      toast.success("History cleared");
    } finally {
      setClearOpen(false);
    }
  };

  const exportData = () => {
    const data = JSON.stringify(history, null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "recommendation_history.json";
    a.click();
    toast.success("History exported");
  };

  return (
    <Layout>
      <PageHeader title="History" description="View past recommendations">
        <Button variant="outline" onClick={exportData} className="gap-2">
          <FileDown className="h-4 w-4" />
          Export
        </Button>
        <Button variant="outline" onClick={() => setClearOpen(true)} className="gap-2 text-destructive">
          <Trash2 className="h-4 w-4" />
          Clear
        </Button>
      </PageHeader>

      {/* Filter */}
      <div className="mb-6 max-w-xs">
        <Select value={filter} onValueChange={setFilter}>
          <SelectTrigger>
            <SelectValue placeholder="Filter by student" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Students</SelectItem>
            {students.map((s) => (
              <SelectItem key={s.id} value={s.id}>
                {s.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* History List */}
      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-6 bg-muted rounded w-1/3 mb-4" />
                <div className="h-4 bg-muted rounded w-2/3" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <EmptyState
          icon={HistoryIcon}
          title="No history yet"
          description="Generated recommendations will appear here"
        />
      ) : (
        <div className="space-y-6">
          {filtered.map((entry, idx) => (
            <Card
              key={entry.id}
              className="animate-fade-in"
              style={{ animationDelay: `${idx * 50}ms` }}
            >
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold">
                      {entry.student_name.charAt(0)}
                    </div>
                    {entry.student_name}
                  </CardTitle>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <User className="h-4 w-4" />
                      {entry.student_id}
                    </span>
                    <span className="flex items-center gap-1">
                      <Calendar className="h-4 w-4" />
                      {new Date(entry.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4">
                  {entry.recommendations.map((rec) => (
                    <div
                      key={rec.topic_id}
                      className="flex items-center gap-4 p-4 bg-muted/50 rounded-lg"
                    >
                      <MatchScore score={rec.match_score} size="sm" />
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded-full">
                            {rec.domain}
                          </span>
                        </div>
                        <h4 className="font-medium">{rec.title}</h4>
                        <p className="text-sm text-muted-foreground line-clamp-1">
                          {rec.description}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Clear Confirmation */}
      <AlertDialog open={clearOpen} onOpenChange={setClearOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Clear History</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to clear all history? This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleClear} className="bg-destructive text-destructive-foreground">
              Clear All
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </Layout>
  );
}
