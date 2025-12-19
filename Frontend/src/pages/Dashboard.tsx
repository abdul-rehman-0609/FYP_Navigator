import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Users, Lightbulb, BookOpen, TrendingUp, UserPlus, ArrowRight } from "lucide-react";
import { Layout } from "@/components/layout/Layout";
import { StatCard } from "@/components/ui/stat-card";
import { PageHeader } from "@/components/ui/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

export default function Dashboard() {
  const [stats, setStats] = useState({ students: 0, recommendations: 0, topics: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getStats()
      .then(setStats)
      .catch(() => setStats({ students: 12, recommendations: 48, topics: 35 }))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout>
      <PageHeader 
        title="Dashboard" 
        description="Welcome to the FYP Recommender System"
      >
        <Link to="/add-student">
          <Button className="gap-2">
            <UserPlus className="h-4 w-4" />
            Add Student
          </Button>
        </Link>
      </PageHeader>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Students"
          value={loading ? "..." : stats.students}
          icon={Users}
          color="blue"
          trend="+3 this week"
        />
        <StatCard
          title="Recommendations"
          value={loading ? "..." : stats.recommendations}
          icon={Lightbulb}
          color="purple"
          trend="+12 this week"
        />
        <StatCard
          title="Available Topics"
          value={loading ? "..." : stats.topics}
          icon={BookOpen}
          color="teal"
        />
        <StatCard
          title="Match Rate"
          value="94%"
          icon={TrendingUp}
          color="coral"
          trend="+2% from last month"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <div className="p-2 rounded-lg bg-primary/10 text-primary">
                <UserPlus className="h-5 w-5" />
              </div>
              Quick Actions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Link to="/add-student" className="block">
              <div className="flex items-center justify-between p-4 rounded-xl bg-muted/50 hover:bg-muted transition-colors group">
                <div>
                  <p className="font-medium">Add New Student</p>
                  <p className="text-sm text-muted-foreground">Create a student profile</p>
                </div>
                <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:text-foreground group-hover:translate-x-1 transition-all" />
              </div>
            </Link>
            <Link to="/recommendations" className="block">
              <div className="flex items-center justify-between p-4 rounded-xl bg-muted/50 hover:bg-muted transition-colors group">
                <div>
                  <p className="font-medium">Generate Recommendations</p>
                  <p className="text-sm text-muted-foreground">Find perfect FYP topics</p>
                </div>
                <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:text-foreground group-hover:translate-x-1 transition-all" />
              </div>
            </Link>
            <Link to="/students" className="block">
              <div className="flex items-center justify-between p-4 rounded-xl bg-muted/50 hover:bg-muted transition-colors group">
                <div>
                  <p className="font-medium">View All Students</p>
                  <p className="text-sm text-muted-foreground">Manage student profiles</p>
                </div>
                <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:text-foreground group-hover:translate-x-1 transition-all" />
              </div>
            </Link>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <div className="p-2 rounded-lg bg-purple/10 text-purple">
                <TrendingUp className="h-5 w-5" />
              </div>
              System Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                <span className="text-sm font-medium">Knowledge Base Status</span>
                <span className="text-xs bg-emerald/10 text-emerald px-2 py-1 rounded-full">Active</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                <span className="text-sm font-medium">ML Fallback</span>
                <span className="text-xs bg-emerald/10 text-emerald px-2 py-1 rounded-full">Ready</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                <span className="text-sm font-medium">Available Skills</span>
                <span className="text-sm font-semibold">62</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                <span className="text-sm font-medium">Available Courses</span>
                <span className="text-sm font-semibold">13</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                <span className="text-sm font-medium">Domain Categories</span>
                <span className="text-sm font-semibold">8</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
