#!/usr/bin/env python3
"""
GitHub Issue Generator Script - YAML Version
تولید خودکار ایشوها از فایل YAML roadmap
"""

import os
import re
import json
import argparse
import hashlib
import yaml
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

import requests
from github import Github
from github.GithubException import GithubException


@dataclass
class Task:
    """Task data structure"""
    title: str
    description: str
    phase: str
    week: int
    day_range: str
    category: str
    priority: str = "medium"
    labels: Optional[List[str]] = None
    assignee: Optional[str] = None
    milestone: Optional[str] = None
    estimated_hours: Optional[float] = None
    subtasks: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.labels is None:
            self.labels = []
        if self.subtasks is None:
            self.subtasks = []


@dataclass
class Phase:
    """Phase data structure"""
    name: str
    description: str
    duration_weeks: int
    tasks: List[Task]
    labels: List[str]
    goals: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.goals is None:
            self.goals = []


class GitHubIssueGenerator:
    """GitHub Issue Generator از YAML roadmap"""
    
    def __init__(self, token: str, repo_owner: str, repo_name: str):
        """
        Initialize GitHub client
        
        Args:
            token: GitHub personal access token
            repo_owner: Repository owner username
            repo_name: Repository name
        """
        self.github = Github(token)
        self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")
        self.token = token
        self.repo_owner = repo_owner
        
    def parse_yaml_roadmap(self, file_path: str) -> List[Phase]:
        """
        Parse YAML roadmap file and extract phases and tasks
        
        Args:
            file_path: Path to YAML roadmap file
            
        Returns:
            List of Phase objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        
        if 'phases' not in data:
            raise ValueError("YAML file must contain 'phases' section")
        
        phases = []
        project_name = data.get('project').get('name')
        if project_name:
            for phase_data in data['phases']:
                phase_name = phase_data.get('name', 'Unknown Phase')
                phase_description = phase_data.get('description', '')
                phase_duration = phase_data.get('duration_weeks', 1)
                phase_goals = phase_data.get('goals', [])
                
                # Extract phase number for labeling
                phase_match = re.search(r'Phase (\d+)', phase_name)
                phase_num = phase_match.group(1) if phase_match else "unknown"
                
                # Create phase labels
                phase_labels = [
                    f"phase-{phase_num}",
                    "backend" if any(keyword in phase_name.lower() for keyword in ['backend', 'api', 'server', 'infrastructure']) else "frontend",
                    phase_name.lower().replace(' ', '-').replace(':', '')
                ]
                
                tasks = []
                weeks_data = phase_data.get('weeks', [])
                
                for week_data in weeks_data:
                    week_number = week_data.get('week_number', 1)
                    week_title = week_data.get('title', f'Week {week_number}')
                    categories = week_data.get('categories', [])
                    
                    for category_data in categories:
                        category_name = category_data.get('category', 'General')
                        # Extract day range from category name
                        day_range_match = re.search(r'\(Day (\d+(?:-\d+)?)\)', category_name)
                        day_range = day_range_match.group(1) if day_range_match else f"{week_number*7-6}-{week_number*7}"
                        
                        # Clean category name
                        clean_category = re.sub(r'\s*\(Day.*?\)', '', category_name).strip()
                        
                        category_tasks = category_data.get('tasks', [])
                        
                        for task_data in category_tasks:
                            task_title = task_data.get('title', 'Untitled Task')
                            task_description_text = task_data.get('description', '')
                            estimated_hours = task_data.get('estimated_hours', 0)
                            task_priority = task_data.get('priority', 'medium')
                            subtasks = task_data.get('subtasks', [])
                            
                            # Generate comprehensive task description

                            task_description = self._generate_yaml_task_description(
                                task_title, task_description_text, phase_name, week_title, 
                                week_number, clean_category, estimated_hours, subtasks, 
                                project_name
                            ) if not "Unknown Project" else ""
                            
                            # Create task labels
                            task_labels = [
                                f"week-{week_number}",
                                clean_category.lower().replace(' ', '-'),
                                task_priority,
                                f"estimate-{int(estimated_hours)}h" if estimated_hours > 0 else "estimate-unknown"
                            ] + phase_labels
                            
                            task = Task(
                                title=task_title,
                                description=task_description,
                                phase=phase_name,
                                week=week_number,
                                day_range=day_range,
                                category=clean_category,
                                priority=task_priority,
                                labels=task_labels,
                                assignee=self.repo_owner,
                                milestone=phase_name,
                                estimated_hours=estimated_hours,
                                subtasks=subtasks
                            )
                            
                            tasks.append(task)
                
                phase = Phase(
                    name=phase_name,
                    description=phase_description,
                    duration_weeks=phase_duration,
                    tasks=tasks,
                    labels=phase_labels,
                    goals=phase_goals
                )
                
                phases.append(phase)

        return phases
    
    def _generate_yaml_task_description(self, title: str, description: str, phase_name: str, 
                                       week_title: str, week_number: int, category: str, 
                                       estimated_hours: float, subtasks: List[str], 
                                       project_name: str) -> str:
        """Generate detailed task description from YAML data with unique signature"""
        signature = self._generate_signature(title, phase_name, week_number)
        
        subtasks_section = ""
        if subtasks:
            subtasks_section = f"""
### Subtasks
"""
            for i, subtask in enumerate(subtasks, 1):
                subtasks_section += f"- [ ] {subtask}\n"
        
        estimate_section = f"**Estimated Hours:** {estimated_hours} hours\n" if estimated_hours > 0 else ""
        
        return f"""<!-- UNIQUE_SIGNATURE: {signature} -->

## Task Overview
**Project:** {project_name}
**Phase:** {phase_name}
**Week:** Week {week_number} - {week_title}
**Category:** {category}
{estimate_section}

### Task Description
{description}

### Primary Goal
{title}
{subtasks_section}

### Acceptance Criteria
- [ ] Code implementation completed according to specifications
- [ ] Unit tests written with >80% coverage
- [ ] Integration tests implemented and passing
- [ ] Code review completed and approved
- [ ] Documentation updated (API docs, README, comments)
- [ ] Security review completed (if applicable)
- [ ] Performance benchmarks met (if applicable)

### Technical Requirements
- Follow Clean Architecture principles
- Implement comprehensive error handling
- Add structured logging with appropriate levels
- Ensure security best practices are followed
- Write maintainable and readable code
- Follow project coding standards and conventions

### Definition of Done
- ✅ All acceptance criteria met
- ✅ Code deployed to staging environment
- ✅ Feature tested by QA/stakeholders
- ✅ Documentation updated and reviewed
- ✅ No blocking bugs or security issues
- ✅ Performance meets requirements

### Closing Instructions
To close this issue automatically, include one of these keywords in your commit message followed by the issue number:
- `close`, `closes`, `closed`
- `fix`, `fixes`, `fixed`
- `resolve`, `resolves`, `resolved`

Example: `git commit -m "Implement {title}, closes #<issue_number>"`

**Note:** The commit must be pushed to the default branch (main/master) to trigger automatic closure.
        """ 
    
    def _determine_task_priority(self, task_title: str, task_data: Dict) -> str:
        """Determine task priority based on title content and YAML data"""
        if task_data and 'priority' in task_data:
            return task_data['priority']
        
        task_lower = task_title.lower()
        
        if any(word in task_lower for word in ['critical', 'urgent', 'security', 'auth', 'authentication']):
            return 'high'
        elif any(word in task_lower for word in ['optimization', 'performance', 'advanced', 'integration']):
            return 'medium'
        elif any(word in task_lower for word in ['documentation', 'comment', 'polish', 'cleanup']):
            return 'low'
        else:
            return 'medium'
    
    def _generate_signature(self, task_title: str, phase_name: str, week_number: int) -> str:
        """Generate a unique signature for the task using hash"""
        unique_string = f"{phase_name}-{week_number}-{task_title}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()
    
    def _issue_exists(self, signature: str) -> bool:
        """Check if an issue with the given signature already exists"""
        query = f"repo:{self.repo.full_name} is:issue \"{signature}\" in:body"
        try:
            issues = self.github.search_issues(query=query)
            return issues.totalCount > 0
        except GithubException as e:
            print(f"❌ Error searching for existing issue with signature {signature}: {e}")
            return False
    
    def save_parsed_to_file(self, phases: List[Phase], file_path: str) -> None:
        """Save parsed phases to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(phase) for phase in phases], f, indent=4, ensure_ascii=False)
        print(f"✅ Parsed data saved to: {file_path}")
    
    def load_parsed_from_file(self, file_path: str) -> List[Phase]:
        """Load parsed phases from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        phases = []
        for p_data in data:
            tasks = [Task(**t_data) for t_data in p_data['tasks']]
            phase = Phase(
                name=p_data['name'],
                description=p_data['description'],
                duration_weeks=p_data['duration_weeks'],
                tasks=tasks,
                labels=p_data['labels'],
                goals=p_data.get('goals', [])
            )
            phases.append(phase)
        print(f"✅ Loaded parsed data from: {file_path}")
        return phases
    
    def create_labels(self, phases: List[Phase]) -> None:
        """Create GitHub labels for phases and categories"""
        standard_labels = [
            {"name": "high", "color": "d73a4a", "description": "High priority task"},
            {"name": "medium", "color": "fbca04", "description": "Medium priority task"},
            {"name": "low", "color": "0075ca", "description": "Low priority task"},
            {"name": "backend", "color": "1d76db", "description": "Backend development"},
            {"name": "frontend", "color": "0e8a16", "description": "Frontend development"},
            {"name": "testing", "color": "5319e7", "description": "Testing related tasks"},
            {"name": "ui-ux", "color": "f9d0c4", "description": "UI/UX design and implementation"},
            {"name": "api", "color": "c2e0c6", "description": "API development"},
            {"name": "database", "color": "fef2c0", "description": "Database related tasks"},
            {"name": "authentication", "color": "d4c5f9", "description": "Authentication and security"},
            {"name": "ai-integration", "color": "ff6b6b", "description": "AI and machine learning"},
            {"name": "devops", "color": "bfd4f2", "description": "DevOps and deployment"},
            {"name": "integration", "color": "c5def5", "description": "External integrations"},
            {"name": "development", "color": "7057ff", "description": "General development"},
            {"name": "documentation", "color": "0052cc", "description": "Documentation tasks"},
            {"name": "sub-task", "color": "00ccff", "description": "Sub-task of a larger issue"},
            {"name": "epic", "color": "8b5cf6", "description": "Epic or coordination issue"},
            {"name": "coordination", "color": "f59e0b", "description": "Coordination task"}
        ]
        
        # Add estimate labels
        for hours in [1, 2, 3, 4, 5, 8, 12, 16, 24, 40]:
            standard_labels.append({
                "name": f"estimate-{hours}h",
                "color": "e5e7eb",
                "description": f"Estimated {hours} hours of work"
            })
        
        standard_labels.append({
            "name": "estimate-unknown",
            "color": "9ca3af",
            "description": "Time estimate not provided"
        })
        
        # Add phase labels
        for phase in phases:
            phase_match = re.search(r'Phase (\d+)', phase.name)
            phase_num = phase_match.group(1) if phase_match else "unknown"
            standard_labels.append({
                "name": f"phase-{phase_num}",
                "color": "b60205" if "Backend" in phase.name or "Infrastructure" in phase.name else "0e8a16",
                "description": f"{phase.name}"
            })
        
        # Add week labels
        week_colors = ["e4e669", "c7e9b4", "7fcdbb", "41b6c4", "1d91c0", 
                      "225ea8", "253494", "081d58", "f03b20", "bd0026"]
        max_weeks = max([phase.duration_weeks for phase in phases] + [10])
        for i in range(1, max_weeks + 1):
            color_index = (i - 1) % len(week_colors)
            standard_labels.append({
                "name": f"week-{i}",
                "color": week_colors[color_index],
                "description": f"Week {i} tasks"
            })
        
        existing_labels = {label.name for label in self.repo.get_labels()}
        for label_data in standard_labels:
            if label_data["name"] not in existing_labels:
                try:
                    self.repo.create_label(
                        name=label_data["name"],
                        color=label_data["color"],
                        description=label_data["description"]
                    )
                    print(f"✅ Created label: {label_data['name']}")
                except GithubException as e:
                    print(f"❌ Failed to create label {label_data['name']}: {e}")
            else:
                print(f"⏭️  Label already exists: {label_data['name']}")
    
    def create_milestones(self, phases: List[Phase]) -> Dict[str, Any]:
        """Create GitHub milestones for phases"""
        milestones = {}
        base_date = datetime.now()
        
        for i, phase in enumerate(phases):
            try:
                weeks_offset = sum(p.duration_weeks for p in phases[:i])
                due_date = base_date + timedelta(weeks=weeks_offset + phase.duration_weeks)
                _goalsstr = f"\nGoals:\n" + "\n".join(f"- {goal}" for goal in phase.goals or '') if phase.goals else ""
                milestone = self.repo.create_milestone(
                    title=phase.name,
                    description=f"{phase.description}\n{_goalsstr}",
                    due_on=due_date
                )
                milestones[phase.name] = milestone
                print(f"✅ Created milestone: {phase.name}")
                
            except GithubException as e:
                if "already_exists" in str(e):
                    for milestone in self.repo.get_milestones():
                        if milestone.title == phase.name:
                            milestones[phase.name] = milestone
                            print(f"⏭️  Milestone already exists: {phase.name}")
                            break
                else:
                    print(f"❌ Failed to create milestone {phase.name}: {e}")
        
        return milestones
    
    def _validate_assignee(self, assignee: str) -> bool:
        """Validate if the assignee is a collaborator in the repository"""
        try:
            collaborators = self.repo.get_collaborators()
            return any(collaborator.login == assignee for collaborator in collaborators)
        except GithubException as e:
            print(f"❌ Error validating assignee {assignee}: {e}")
            return False
    
    def create_issues(self, phases: List[Phase], milestones: Dict[str, Any], max_tasks: int) -> List[Dict[str, Any]]:
        """Create GitHub issues from tasks, with sub-tasks as linked sub-issues"""
        created_issues = []
        skipped_issues = []
        task_count = 0
        
        for phase in phases:
            print(f"\n🚀 Processing issues for {phase.name}...")
            
            for task in phase.tasks:
                if task_count >= max_tasks:
                    print(f"⏹️ Reached maximum task limit ({max_tasks}). Stopping issue creation.")
                    break
                
                # Generate signature and check for duplicates
                signature = self._generate_signature(task.title, task.phase, task.week)
                if self._issue_exists(signature):
                    print(f"⏭️ Skipped duplicate issue: {task.title} (signature: {signature})")
                    skipped_issues.append(task.title)
                    continue
                
                task_count += 1
                
                try:
                    milestone = milestones.get(task.milestone or "")
                    
                    # Determine assignee
                    assignee = task.assignee if task.assignee and self._validate_assignee(task.assignee) else self.repo_owner
                    
                    if task.subtasks:
                        # Create main epic issue first, without subtasks in description
                        main_description = self._generate_yaml_task_description(
                            task.title, task.description, task.phase, f"Week {task.week}", 
                            task.week, task.category, float(task.estimated_hours or 0.0), [], "Unknown Project"
                        ) + "\n\nThis is an epic issue. Sub-issues will be linked below."
                        
                        main_labels = task.labels or[] + ['epic', 'coordination']
                        
                        main_issue_kwargs = {
                            "title": f"{task.title} (Coordination)",
                            "body": main_description,
                            "labels": main_labels,
                            "assignee": assignee
                        }
                        if milestone is not None:
                            main_issue_kwargs["milestone"] = milestone
                        
                        main_issue = self.repo.create_issue(**main_issue_kwargs)
                        
                        created_issues.append({
                            'number': main_issue.number,
                            'title': main_issue.title,
                            'url': main_issue.html_url,
                            'phase': task.phase,
                            'week': task.week,
                            'estimated_hours': 0  # Coordination has no direct hours
                        })
                        
                        print(f"✅ Created main issue #{main_issue.number}: {main_issue.title} (0h)")
                        
                        sub_issues = []
                        sub_estimated_hours = task.estimated_hours / len(task.subtasks) if task.estimated_hours and len(task.subtasks) > 0 else 0
                        
                        for i, subtask_desc in enumerate(task.subtasks, 1):
                            sub_title = f"Subtask {i}: {subtask_desc} (part of {task.title})"
                            sub_signature = self._generate_signature(sub_title, task.phase, task.week)
                            if self._issue_exists(sub_signature):
                                print(f"⏭️ Skipped duplicate sub-issue: {sub_title} (signature: {sub_signature})")
                                skipped_issues.append(sub_title)
                                continue
                            
                            sub_description = self._generate_yaml_task_description(
                                sub_title, subtask_desc, task.phase, f"Week {task.week}", 
                                task.week, task.category, sub_estimated_hours, [], "Unknown Project"
                            ) + f"\n\nThis is a sub-issue of #{main_issue.number}"
                            
                            sub_labels = task.labels or [] + ['sub-task']
                            
                            sub_issue_kwargs = {
                                "title": sub_title,
                                "body": sub_description,
                                "labels": sub_labels,
                                "assignee": assignee
                            }
                            if milestone is not None:
                                sub_issue_kwargs["milestone"] = milestone
                            
                            sub_issue = self.repo.create_issue(**sub_issue_kwargs)
                            
                            sub_issues.append((sub_issue.number, subtask_desc))
                            
                            created_issues.append({
                                'number': sub_issue.number,
                                'title': sub_issue.title,
                                'url': sub_issue.html_url,
                                'phase': task.phase,
                                'week': task.week,
                                'estimated_hours': sub_estimated_hours
                            })
                            
                            print(f"✅ Created sub-issue #{sub_issue.number}: {sub_title} ({sub_estimated_hours}h)")
                        
                        # Update main issue with sub-issues list
                        if sub_issues:
                            sub_section = "### Sub-issues\n" + "\n".join(f"- [ ] [#{num}] {desc}" for num, desc in sub_issues)
                            updated_body = main_issue.body + "\n\n" + sub_section
                            main_issue.edit(body=updated_body)
                            print(f"✅ Updated main issue #{main_issue.number} with sub-issues links")
                    else:
                        # No subtasks, create single issue
                        issue_kwargs = {
                            "title": task.title,
                            "body": task.description,
                            "labels": task.labels,
                            "assignee": assignee
                        }
                        if milestone is not None:
                            issue_kwargs["milestone"] = milestone
                        
                        issue = self.repo.create_issue(**issue_kwargs)
                        
                        created_issues.append({
                            'number': issue.number,
                            'title': issue.title,
                            'url': issue.html_url,
                            'phase': task.phase,
                            'week': task.week,
                            'estimated_hours': task.estimated_hours
                        })
                        
                        print(f"✅ Created issue #{issue.number}: {task.title} ({task.estimated_hours}h)")
                
                except GithubException as e:
                    print(f"❌ Failed to create issue for '{task.title}': {e}")
        
        total_hours = sum(issue.get('estimated_hours', 0) for issue in created_issues)
        print(f"\n📊 Issues Summary: Created {len(created_issues)}, Skipped {len(skipped_issues)} duplicates")
        print(f"📊 Total Estimated Hours: {total_hours} hours")
        return created_issues
    
    def generate_summary_report(self, phases: List[Phase], created_issues: List[Dict[str, Any]]) -> str:
        """Generate summary report of created issues"""
        total_estimated_hours = sum(issue.get('estimated_hours', 0) for issue in created_issues)
        
        report = f"""# GitHub Issues Creation Report - YAML Roadmap
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Repository:** {self.repo.full_name}

## Summary
- **Total Phases:** {len(phases)}
- **Total Tasks Processed:** {sum(len(phase.tasks) for phase in phases)}
- **Created Issues:** {len(created_issues)}
- **Total Estimated Hours:** {total_estimated_hours} hours

## Created Issues by Phase

"""
        
        for phase in phases:
            phase_issues = [issue for issue in created_issues if issue['phase'] == phase.name]
            phase_hours = sum(issue.get('estimated_hours', 0) for issue in phase_issues)
            report += f"### {phase.name}\n"
            report += f"**Issues Created:** {len(phase_issues)}\n"
            report += f"**Estimated Hours:** {phase_hours} hours\n"
            report += f"**Duration:** {phase.duration_weeks} weeks\n\n"
            
            for issue in phase_issues:
                hours_info = f" ({issue.get('estimated_hours', 0)}h)" if issue.get('estimated_hours') else ""
                report += f"- [#{issue['number']}]({issue['url']}) {issue['title']} (Week {issue['week']}){hours_info}\n"
            
            report += "\n"
        
        return report


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate GitHub issues from YAML roadmap')
    parser.add_argument('--token', required=True, help='GitHub personal access token')
    parser.add_argument('--repo', required=True, help='Repository in format owner/repo-name')
    parser.add_argument('--file', help='Path to YAML roadmap file')
    parser.add_argument('--output', help='Output file for summary report')
    parser.add_argument('--dry-run', action='store_true', help='Parse only, do not create issues')
    parser.add_argument('--from-parsed', help='Load parsed phases from JSON file instead of parsing YAML')
    
    args = parser.parse_args()
    
    try:
        repo_owner, repo_name = args.repo.split('/')
    except ValueError:
        print("❌ Repository format should be: owner/repo-name")
        return
    
    generator = GitHubIssueGenerator(args.token, repo_owner, repo_name)
    print(f"🚀 Connected to repository: {args.repo}")
    
    try:
        if args.from_parsed:
            if not Path(args.from_parsed).exists():
                print(f"❌ File not found: {args.from_parsed}")
                return
            phases = generator.load_parsed_from_file(args.from_parsed)
        else:
            if not args.file or not Path(args.file).exists():
                print(f"❌ File not found: {args.file}")
                return
            print("📖 Parsing YAML roadmap...")
            phases = generator.parse_yaml_roadmap(args.file)
            total_tasks = sum(len(p.tasks) for p in phases)
            total_hours = sum(sum(task.estimated_hours or 0 for task in p.tasks) for p in phases)
            print(f"✅ Found {len(phases)} phases with {total_tasks} tasks ({total_hours} estimated hours)")
            
            save_response = input("Do you want to save the parsed data in JSON? (y/n): ").strip().lower()
            if save_response == 'y':
                save_file = input("Enter filename to save (default: parsed_phases.json): ").strip() or 'parsed_phases.json'
                generator.save_parsed_to_file(phases, save_file)
        
        total_tasks = sum(len(phase.tasks) for phase in phases)
        if args.dry_run:
            print("\n🔍 DRY RUN - No issues will be created")
            for phase in phases:
                print(f"\nPhase: {phase.name} ({phase.duration_weeks} weeks)")
                print(f"Tasks: {len(phase.tasks)}")
                phase_hours = sum(task.estimated_hours or 0 for task in phase.tasks)
                print(f"Estimated Hours: {phase_hours}")
                for task in phase.tasks[:3]:
                    hours_info = f" ({task.estimated_hours}h)" if task.estimated_hours else ""
                    print(f"  - {task.title}{hours_info}")
                if len(phase.tasks) > 3:
                    print(f"  ... and {len(phase.tasks) - 3} more tasks")
            return
        
        # Prompt for number of tasks to convert to issues
        max_tasks = total_tasks
        prompt = f"You have {total_tasks} tasks. How many tasks do you want to create as GitHub issues? (1-{total_tasks}, default {total_tasks}): "
        try:
            task_limit = input(prompt).strip()
            max_tasks = int(task_limit) if task_limit else total_tasks
            if max_tasks < 1 or max_tasks > total_tasks:
                raise ValueError
        except ValueError:
            print(f"❌ Invalid input. Using default: {total_tasks} tasks")
            max_tasks = total_tasks
        
        create_response = input("Do you want to create issues in GitHub? (y/n): ").strip().lower()
        if create_response != 'y':
            print("❌ Aborting issue creation.")
            return
        
        print("\n🏷️  Creating labels...")
        generator.create_labels(phases)
        
        print("\n🎯 Creating milestones...")
        milestones = generator.create_milestones(phases)
        
        print("\n📝 Creating issues...")
        created_issues = generator.create_issues(phases, milestones, max_tasks)
        
        report = generator.generate_summary_report(phases, created_issues)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📊 Report saved to: {args.output}")
        else:
            print("\n" + "="*50)
            print(report)
        
        print(f"\n🎉 Successfully created {len(created_issues)} issues!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


# Usage: python github_issue_gen/yaml_issue_gen.py --token YOUR_TOKEN --repo owner/repo-name --file roadmap.yaml --output report.md
if __name__ == "__main__":
    main()