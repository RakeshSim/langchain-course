	clone
(base) rakeshyadav@Rakeshs-MacBook-Pro agent-under-hood % git clone https://github.com/RakeshSim/langchain-course.git
Cloning into 'langchain-course'...
remote: Enumerating objects: 319, done.
remote: Counting objects: 100% (319/319), done.
remote: Compressing objects: 100% (167/167), done.
remote: Total 319 (delta 145), reused 313 (delta 139), pack-reused 0 (from 0)
Receiving objects: 100% (319/319), 3.41 MiB | 13.59 MiB/s, done.
Resolving deltas: 100% (145/145), done.
(base) rakeshyadav@Rakeshs-MacBook-Pro agent-under-hood % ls
langchain-course
(base) rakeshyadav@Rakeshs-MacBook-Pro agent-under-hood % cd langchain-course 
(base) rakeshyadav@Rakeshs-MacBook-Pro langchain-course % ls
LICENSE		README.md	static
(base) rakeshyadav@Rakeshs-MacBook-Pro langchain-course % rm -rf *
zsh: sure you want to delete all 3 files in /Users/rakeshyadav/TCS-AI-Training/LangChanin-Course/agent-under-hood/langchain-course [yn]? y
(base) rakeshyadav@Rakeshs-MacBook-Pro langchain-course % 
(base) rakeshyadav@Rakeshs-MacBook-Pro langchain-course % ls
(base) rakeshyadav@Rakeshs-MacBook-Pro langchain-course % uv init
Initialized project `langchain-course`
(base) rakeshyadav@Rakeshs-MacBook-Pro langchain-course % uv add langchain langchain-openai langchain-tavily tavily-python python-dotenv black isort
