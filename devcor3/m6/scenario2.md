# Problem
Wired Brain Coffee company is an international conglomerate that sells a
variety of coffee products to customers worldwide. As a "product company",
Wired Brain Coffee is looking to grow by increasing its product sales using
two concurrent strategies. It will develop new products and sell them to
existing customers, while also targeting customers in emerging markets using
it's existing high-runner products. To accomplish this, their internal
point-of-sale and order processing systems need to be benchmarked for growth.

Most of the engineers believe that the IT infrastructure, especially the
computing environment, will need to grow drastically in order to support
concurrent product development AND market development strategies. Top
management isn't convinced that the infrastructure needs to grow, and is
unwilling to make new investments without clear data indicating otherwise.
Today, the team uses traditional monitoring tools, like an up/down status map
and basic SNMP polling, which is enough to track the "vitals" of the
infrastructure. However, it doesn't provide compelling evidence in the context
of investment justification.

Since the system administrators have full access to everything in the
infrastructure, they are willing to install additional software packages onto
their systems if it will bring broader and deeper metric collection. The IT
administrators are also technically skilled and aren't afraid to work with
complex, enterprise-grade orchestration products if it will improve their
ability to manage their systems. Even aside from the investment justification,
the team has the foresight to know that they'll be managing a much larger
infrastructure in the future. Having an automated configuration management
process would be a huge advantage, and probably necessary for success.

Although management is stingy with money, they don't add needless approvals
into IT processes. The IT administrators can make any change wherever they see
fit, provided the change passes their extensive test process. It's a
collection of automated tests that get run manually before changes are made.
The team knows that if they can set up their environment for declarative,
infrastructure as code management, while concurrently collecting more detailed
performance information from their systems, they'll be able to meet all the
demands of the business. Can you recommend a path forward for Wired Brain Coffee?

# Analysis
Unlike the previous scenario, the concern isn't about reducing cost, but
growing sales. Undertaking multiple concurrent sales strategies is sure to put
on a strain on the IT infrastructure, but management needs to see proof first.

As discussed previously, agents are small software packages that can
be installed on systems to provide additional monitoring details. Often this
is far more effective than SNMP and would help get the information that
management needs regarding system utilization and performance. Independent
streaming telemetry solutions could work, too.

Again, unlike the previous scenario, there are no bureaucrats standing in our
way, so perhaps we can consider continuous deployment. Additionally, they
already have tests written, but run them manually, so migrating these to a CI
pipeline should be easy.

# Solution
You'll notice that, at a glance, the solution looks very similar to scenario
1, and this is deliberate. The general flow for infrastructure is code is the
same regardless of the tooling used, although a few steps may change. In this
case, our highly-skilled administrators will be writing Puppet code. I think
Puppet makes more sense than Ansible for this customer since the agent-based
monitoring on their servers should result in better data collection and
monitoring. Once again, the administrators can push their code to a remote
git repository like GitHub, which kicks off a Travis CI pipeline run.
Considering this customer already had strong automated testing that was run
manually, retooling the tests to work in a CI service like Travis should be
simple.

Additionally, we can use continuous deployment to automatically deploy
updates based on the puppet manifest. Maybe the CD system is still Travis, but
it can run a script containing the proper "puppet" commands. This would
rapidly enable changes to the architecture. Even when changes aren't being
made, the team can collect the data they need to justify expanding their
compute environment. If you chose an agentless solution like Ansible or failed
to include continuous deployment in your proposed solution, you should mark
this scenario for follow-up.
