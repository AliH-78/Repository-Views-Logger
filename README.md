<h2>Repository Views Logger</h2>

<h3> What is it? </h3>
<p>Repository views logger is a log system that can be used for storing GitHub repository traffic datas more than 15 days.<br>There may be a few bugs as it is still developing.</p>

<h3> How to use it? </h3>
<p>There is an example usage below:<br><code>python main.py --token "gh_token" --repository-name "user_name/user_repository" --log-repository-views</code><br><br>After executing the command, script will start to log specified repository's view with one day apart if sent token has enough permission to that.</p>
