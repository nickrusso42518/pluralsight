# Problem
Imagine you work for a large, global service provider named Globomantics. I'm
reusing the Globomantics name for this scenario. It's unrelated to the
previous Globomantics content we've explored throughout the learning path. The
company is facing pressure from investors to improve profitability. Top
management has decided that the best strategy is a mix of cost reduction and
cost avoidance, as growing sales in a stale market is notoriously difficult.

As an internationally-operated network, there are extensive policies on how
configuration management works. Adding new network services, such as
connectivity between customer sites or turning up new circuits, only requires
approval from the network operations manager. She reviews new service requests
at least once a week. Permanent infrastructure changes must be approved by a
bureaucratic committee that convenes quarterly.

Today, the organization has many high-wage, low-skill contractors manually
configuring devices by following standardized work procedures that are
relatively accurate. Occasional human errors cause network outages for
customers, though. These contractors have entry level network and system
administration skills. They also know how to navigate a Bash shell and edit
text files. Most of them have basic HTTP knowledge given their experience in
hosting a web portal for customer support tickets. A handful have worked with
REST-style APIs, too. None of them have any experience with programming
languages.

The IT operations vice president, who is responsible for all things IT, wants
to somehow manage this network infrastructure in a more declarative way
without needing professional programmers. He wants a model-driven approach
that will be relevant many years into the future. Given these business
requirements and corresponding technical constraints, what solution would you
recommend? Try to define the general process and components first, then try to
assign specific products to fit each role.

# Analysis
The business goal is to improve profitability, and the mechanism to achieve
this goal is cost reduction and cost avoidance. For those unfamiliar with
these terms, cost reduction means reducing the current amount of money being
spent by the company. Cost avoidance means rejecting new costs, such as hiring
new people or making new capital investments.

Given the complex red tape surrounding international IT operations, using
continuous deployment is probably not feasible. Everything needs to be
approved by a non-technical human, rather than a well-informed machine.
However, if you're thinking maybe we can do continuous integration with a
manual deployment step, you're on the right track. Recall that despite having
standardized work, humans still make mistakes, so transforming all test
procedures into a CI pipeline is a smart idea.

In terms of infrastructure as code solutions, it needs to be relatively
simple, generally something that doesn't require writing code in a traditional
programming language.

# Solution
Your solution may be a bit different, but give yourself credit if your
solution is conceptually comparable. I'd recommend using Ansible with RESTCONF
for infrastructure as code. This is a modern, model-driven approach that
doesn't require writing any Python code. The existing RESTCONF modules are
well documented and generally work well, open bugs notwithstanding. If the
company is willing to terminate employees who are no longer needed, this would
reduce labor costs. If the company doesn't want to punish employees for
contributing to productivity improvements, cost avoidance is achieved because
the number of issues in production should be reduced using CI.

The automation solution may obviate the need to hire additional employees in
the future. Any CI solution will do, but we've explored Travis extensively in
this course, so I'm depicting that. Other great solutions include Gitlab CI or
AWS CodePipeline. If you suggested using custom Python scripts, SSH or SNMP
based management, continuous deployment, or other solutions that violate a
given constraint, you should mark this challenge for follow-up to remediate.
