import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Search, UserPlus, Eye, Edit, Trash2, Users, GraduationCap } from "lucide-react";
import { Layout } from "@/components/layout/Layout";
import { PageHeader } from "@/components/ui/page-header";
import { EmptyState } from "@/components/ui/empty-state";
import { SkillBadge } from "@/components/ui/skill-badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
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
import { api, Student } from "@/lib/api";
import { toast } from "sonner";

export default function Students() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);
  const [deleteId, setDeleteId] = useState<string | null>(null);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const data = await api.getStudents();
      setStudents(data);
    } catch {
      // Mock data fallback
      setStudents([
        {
          id: "STU001",
          name: "Ahmad Khan",
          cgpa: 3.5,
          major: "Computer Science",
          year: 4,
          skills: [
            { name: "Python", proficiency: "ADVANCED" },
            { name: "Machine Learning", proficiency: "INTERMEDIATE" },
          ],
          interests: [{ domain: "Artificial Intelligence", level: "HIGH" }],
          completed_courses: ["Data Structures", "Artificial Intelligence"],
          preferences: { max_weekly_hours: 20, team_size: 2, preferred_domains: ["AI"] },
        },
        {
          id: "STU002",
          name: "Sara Ahmed",
          cgpa: 3.8,
          major: "Software Engineering",
          year: 4,
          skills: [
            { name: "JavaScript", proficiency: "EXPERT" },
            { name: "React", proficiency: "ADVANCED" },
          ],
          interests: [{ domain: "Web Development", level: "VERY_HIGH" }],
          completed_courses: ["Web Engineering", "Database Systems"],
          preferences: { max_weekly_hours: 25, team_size: 3, preferred_domains: ["Web"] },
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteId) return;
    try {
      await api.deleteStudent(deleteId);
      setStudents(students.filter((s) => s.id !== deleteId));
      toast.success("Student deleted successfully");
    } catch {
      toast.error("Failed to delete student");
    } finally {
      setDeleteId(null);
    }
  };

  const filtered = students.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.id.toLowerCase().includes(search.toLowerCase()) ||
      s.major.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Layout>
      <PageHeader title="Students" description="Manage student profiles">
        <Link to="/add-student">
          <Button className="gap-2">
            <UserPlus className="h-4 w-4" />
            Add Student
          </Button>
        </Link>
      </PageHeader>

      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search by name, ID, or major..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-10 max-w-md"
        />
      </div>

      {/* Students Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-6 bg-muted rounded w-3/4 mb-4" />
                <div className="h-4 bg-muted rounded w-1/2 mb-2" />
                <div className="h-4 bg-muted rounded w-2/3" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <EmptyState
          icon={Users}
          title="No students found"
          description={search ? "Try adjusting your search" : "Add your first student to get started"}
        >
          <Link to="/add-student">
            <Button>Add Student</Button>
          </Link>
        </EmptyState>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((student, idx) => (
            <Card
              key={student.id}
              className="hover:shadow-lg transition-all duration-300 animate-fade-in"
              style={{ animationDelay: `${idx * 50}ms` }}
            >
              <CardContent className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-display font-bold">
                      {student.name.charAt(0)}
                    </div>
                    <div>
                      <h3 className="font-semibold">{student.name}</h3>
                      <p className="text-sm text-muted-foreground">{student.id}</p>
                    </div>
                  </div>
                  <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full font-medium">
                    Year {student.year}
                  </span>
                </div>

                <div className="space-y-3 mb-4">
                  <div className="flex items-center gap-2 text-sm">
                    <GraduationCap className="h-4 w-4 text-muted-foreground" />
                    <span>{student.major}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-muted-foreground">CGPA:</span>
                    <span className="font-semibold">{student.cgpa.toFixed(2)}</span>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1.5 mb-4">
                  {student.skills.slice(0, 3).map((skill) => (
                    <SkillBadge
                      key={skill.name}
                      skill={skill.name}
                      proficiency={skill.proficiency}
                      size="sm"
                    />
                  ))}
                  {student.skills.length > 3 && (
                    <span className="text-xs text-muted-foreground px-2 py-0.5">
                      +{student.skills.length - 3} more
                    </span>
                  )}
                </div>

                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1"
                    onClick={() => setSelectedStudent(student)}
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    View
                  </Button>
                  <Link to={`/add-student?edit=${student.id}`} className="flex-1">
                    <Button variant="outline" size="sm" className="w-full">
                      <Edit className="h-4 w-4 mr-1" />
                      Edit
                    </Button>
                  </Link>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setDeleteId(student.id)}
                    className="text-destructive hover:text-destructive"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* View Dialog */}
      <Dialog open={!!selectedStudent} onOpenChange={() => setSelectedStudent(null)}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold">
                {selectedStudent?.name.charAt(0)}
              </div>
              {selectedStudent?.name}
            </DialogTitle>
            <DialogDescription>
              {selectedStudent?.id} • {selectedStudent?.major} • Year {selectedStudent?.year}
            </DialogDescription>
          </DialogHeader>

          {selectedStudent && (
            <div className="space-y-6 mt-4">
              <div>
                <h4 className="font-semibold mb-2">Academic Info</h4>
                <div className="grid grid-cols-2 gap-4 p-4 bg-muted/50 rounded-lg">
                  <div>
                    <span className="text-sm text-muted-foreground">CGPA</span>
                    <p className="font-semibold">{selectedStudent.cgpa.toFixed(2)}</p>
                  </div>
                  <div>
                    <span className="text-sm text-muted-foreground">Year</span>
                    <p className="font-semibold">{selectedStudent.year}</p>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="font-semibold mb-2">Skills</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedStudent.skills.map((skill) => (
                    <SkillBadge
                      key={skill.name}
                      skill={skill.name}
                      proficiency={skill.proficiency}
                    />
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-semibold mb-2">Interests</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedStudent.interests.map((interest) => (
                    <span
                      key={interest.domain}
                      className="px-3 py-1 bg-purple/10 text-purple rounded-full text-sm"
                    >
                      {interest.domain} ({interest.level})
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-semibold mb-2">Completed Courses</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedStudent.completed_courses.map((course) => (
                    <span
                      key={course}
                      className="px-3 py-1 bg-teal/10 text-teal rounded-full text-sm"
                    >
                      {course}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-semibold mb-2">Preferences</h4>
                <div className="grid grid-cols-2 gap-4 p-4 bg-muted/50 rounded-lg">
                  <div>
                    <span className="text-sm text-muted-foreground">Weekly Hours</span>
                    <p className="font-semibold">{selectedStudent.preferences.max_weekly_hours}h</p>
                  </div>
                  <div>
                    <span className="text-sm text-muted-foreground">Team Size</span>
                    <p className="font-semibold">{selectedStudent.preferences.team_size}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation */}
      <AlertDialog open={!!deleteId} onOpenChange={() => setDeleteId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Student</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete this student? This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground">
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </Layout>
  );
}
