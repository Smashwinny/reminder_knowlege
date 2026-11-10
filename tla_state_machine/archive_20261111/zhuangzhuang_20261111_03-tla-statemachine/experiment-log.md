# TLA+状态机真实实验日志

时间统一Asia/Shanghai（UTC+8）。本项仅合成订单，无支付接口、真实订单或付费API。

## 来源与环境准备的真实执行摘要
- 首先git ls-remote https://github.com/Smashwinny/reminder_knowlege refs/heads/main，返回a8674777e18302b8804b137212b1396cbfe5a747；未更新，仅只读复用旧快照。
- 搜索先命中backnotprop/pstack；实读README发现它是standalone mirror，固定08547969e1dffaa6457ea65141cc62c1d9a2eef1，已改名mirror-discovery作发现线索，不冒充原作者仓库。
- 随后git clone --depth 1 --filter=blob:none --sparse --branch main https://github.com/cursor/plugins upstream，再sparse-checkout set pstack；成功，官方main固定de8ee15dd1194627d21eb5fcd41cb1873208dabb。
- 原系统command -v java/javac均无结果。只在本项tools解压Temurin21.0.13+9 JRE；52,181,297字节，SHA256与发布方校验文件及GitHub资产digest相同。未改系统Java、PATH或安全设置。
- 官方TLC v1.7.4 jar下载成功；2,274,532字节；发布正文SHA1核对通过，并记录本地SHA256，见sources/toolchain.json。不把SHA1说成强签名认证。
- 第一次宽泛文件检索输出过大，最后因不存在根LICENSE退出2；改为定向确认pstack/LICENSE成功。这不是形式化实验失败。
- 原帖与第一层引用已得到全文；第二层发布帖两次请求仍只返回截断正文，记录为部分可读，不补写缺失文字。两张配图已Read：状态图为假想通知例子，发布帖配图只是猫图。

## 2026-11-11T01:27:49.294487+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine`

```sh
tools/jdk-21.0.13+9-jre/bin/java -XX:+UseParallelGC -jar tools/tla2tools.jar -help
```

真实输出：
```text

[1mNAME[0m

	TLC - provides model checking and simulation of TLA+ specifications - Version 2.19 of 08 August 2024


[1mSYNOPSIS[0m

	[1mTLC[0m [[1m-h[0m] [[1m-cleanup[0m] [[1m-continue[0m] [[1m-deadlock[0m] [[1m-debug[0m] [[1m-difftrace[0m] [[1m-generateSpecTE[0m [nomonolith]] [[1m-gzip[0m] [[1m-nowarning[0m] [[1m-terse[0m] [[1m-tool[0m] [[1m-view[0m] [[1m-checkpoint[0m [3mminutes[0m] [[1m-config[0m [3mfile[0m] [[1m-coverage[0m [3mminutes[0m] [[1m-dfid[0m [3mnum[0m] [[1m-dump[0m [dot actionlabels,colorize,snapshot] [3mfile[0m] [[1m-fp[0m [3mN[0m] [[1m-fpbits[0m [3mnum[0m] [[1m-fpmem[0m [3mnum[0m] [[1m-maxSetSize[0m [3mnum[0m] [[1m-metadir[0m [3mpath[0m] [[1m-recover[0m [3mid[0m] [[1m-userFile[0m [3mfile[0m] [[1m-workers[0m [3mnum[0m] SPEC
	[1mTLC[0m [[1m-h[0m] [[1m-cleanup[0m] [[1m-continue[0m] [[1m-deadlock[0m] [[1m-debug[0m] [[1m-difftrace[0m] [[1m-generateSpecTE[0m [nomonolith]] [[1m-gzip[0m] [[1m-nowarning[0m] [[1m-terse[0m] [[1m-tool[0m] [[1m-aril[0m [3mnum[0m] [[1m-checkpoint[0m [3mminutes[0m] [[1m-config[0m [3mfile[0m] [[1m-coverage[0m [3mminutes[0m] [[1m-depth[0m [3mnum[0m] [[1m-dump[0m [dot actionlabels,colorize,snapshot] [3mfile[0m] [[1m-fp[0m [3mN[0m] [[1m-fpbits[0m [3mnum[0m] [[1m-fpmem[0m [3mnum[0m] [[1m-maxSetSize[0m [3mnum[0m] [[1m-metadir[0m [3mpath[0m] [[1m-recover[0m [3mid[0m] [[1m-seed[0m [3mnum[0m] [[1m-userFile[0m [3mfile[0m] [[1m-workers[0m [3mnum[0m] -simulate [file=X,num=Y] SPEC

[1mDESCRIPTION[0m

	The model checker ([1mTLC[0m) provides the functionalities of model checking
	or simulation of TLA+ specifications. It may be invoked from the command
	line, or via the model checking functionality of the Toolbox.
	
	By default, [1mTLC[0m starts in the model checking mode using breadth-first
	approach for the state space exploration.

[1mOPTIONS[0m

	[1m-aril[0m [3mnum[0m
		adjust the seed for random simulation; defaults to 0
	[1m-checkpoint[0m [3mminutes[0m
		interval between check point; defaults to 30
	[1m-cleanup[0m
		clean up the states directory
	[1m-config[0m [3mfile[0m
		provide the configuration file; defaults to SPEC.cfg
	[1m-continue[0m
		continue running even when an invariant is violated; default
		behavior is to halt on first violation
	[1m-coverage[0m [3mminutes[0m
		interval between the collection of coverage information;
		if not specified, no coverage will be collected
	[1m-deadlock[0m
		if specified DO NOT CHECK FOR DEADLOCK. Setting the flag is
		the same as setting CHECK_DEADLOCK to FALSE in config
		file. When -deadlock is specified, config entry is
		ignored; default behavior is to check for deadlocks
	[1m-debug[0m
		print various debugging information - not for production use
		
	[1m-depth[0m [3mnum[0m
		specifies the depth of random simulation; defaults to 100
	[1m-dfid[0m [3mnum[0m
		run the model check in depth-first iterative deepening
		starting with an initial depth of 'num'
	[1m-difftrace[0m
		show only the differences between successive states when
		printing trace information; defaults to printing
		full state descriptions
	[1m-dump[0m [3mfile[0m
		dump all states into the specified file; this parameter takes
		optional parameters for dot graph generation. Specifying
		'dot' allows further options, comma delimited, of zero
		or more of 'actionlabels', 'colorize', 'snapshot' to be
		specified before the '.dot'-suffixed filename
	[1m-fp[0m [3mN[0m
		use the Nth irreducible polynomial from the list stored
		in the class FP64
	[1m-fpbits[0m [3mnum[0m
		the number of MSB used by MultiFPSet to create nested
		FPSets; defaults to 1
	[1m-fpmem[0m [3mnum[0m
		a value in (0.0,1.0) representing the ratio of total
		physical memory to devote to storing the fingerprints
		of found states; defaults to 0.25
	[1m-generateSpecTE[0m
		if errors are encountered during model checking, generate
		a SpecTE tla/cfg file pair which encapsulates Init-Next
		definitions to specify the state conditions of the error
		state; this enables 'tool' mode. The generated SpecTE
		will include tool output as well as all non-Standard-
		Modules dependencies embeded in the module. To prevent
		the embedding of dependencies, add the parameter
		'nomonolith' to this declaration
	[1m-gzip[0m
		control if gzip is applied to value input/output streams;
		defaults to 'off'
	[1m-h[0m
		display these help instructions
	[1m-maxSetSize[0m [3mnum[0m
		the size of the largest set which TLC will enumerate; defaults
		to 1000000 (10^6)
	[1m-metadir[0m [3mpath[0m
		specify the directory in which to store metadata; defaults to
		SPEC-directory/states if not specified
	[1m-nowarning[0m
		disable all warnings; defaults to reporting warnings
	[1m-recover[0m [3mid[0m
		recover from the checkpoint with the specified id
	[1m-seed[0m [3mnum[0m
		provide the seed for random simulation; defaults to a
		random long pulled from a pseudo-RNG
	[1m-simulate[0m
		run in simulation mode; optional parameters may be specified
		comma delimited: 'num=X' where X is the maximum number of
		total traces to generate and/or 'file=Y' where Y is the
		absolute-pathed prefix for trace file modules to be written
		by the simulation workers; for example Y='/a/b/c/tr' would
		produce, e.g, '/a/b/c/tr_1_15'
	[1m-terse[0m
		do not expand values in Print statements; defaults to
		expanding values
	[1m-tool[0m
		run in 'tool' mode, surrounding output with message codes;
		if '-generateSpecTE' is specified, this is enabled
		automatically
	[1m-userFile[0m [3mfile[0m
		an absolute path to a file in which to log user output (for
		example, that which is produced by Print)
	[1m-view[0m
		apply VIEW (if provided) when printing out states
	[1m-workers[0m [3mnum[0m
		the number of TLC worker threads; defaults to 1. Use 'auto'
		to automatically select the number of threads based on the
		number of available cores.

[1mTIPS[0m

	When using the  '-generateSpecTE' you can version the generated specification by doing:
		./tla2tools.jar -generateSpecTE MySpec.tla && NAME="SpecTE-$(date +%s)" && sed -e "s/MODULE SpecTE/MODULE $NAME/g" SpecTE.tla > $NAME.tla

	If, while checking a SpecTE created via '-generateSpecTE', you get an error message concerning
	CONSTANT declaration and you've previous used 'integers' as model values, rename your
	model values to start with a non-numeral and rerun the model check to generate a new SpecTE.

	If, while checking a SpecTE created via '-generateSpecTE', you get a warning concerning
	duplicate operator definitions, this is likely due to the 'monolith' specification
	creation. Try re-running TLC adding the 'nomonolith' option to the '-generateSpecTE'
	parameter.


```
退出码：1

## 2026-11-11T01:29:11.139554+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine/exercise`

```sh
python3 run_labs.py bug
```

真实输出：
```text
实际命令： /workspace/learn-batch/03-tla-statemachine/tools/jdk-21.0.13+9-jre/bin/java -Xmx256m -XX:+UseParallelGC -jar /workspace/learn-batch/03-tla-statemachine/tools/tla2tools.jar -workers 1 -fp 0 -config OrderBug.cfg -metadir /workspace/learn-batch/03-tla-statemachine/exercise/results/bug-meta -dump dot,actionlabels /workspace/learn-batch/03-tla-statemachine/exercise/results/bug-graph.dot OrderBug.tla 
工作目录： /workspace/learn-batch/03-tla-statemachine/exercise/models
TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
Running breadth-first search Model-Checking with fp 0 and seed 3578897609871659003 with 1 worker on 8 cores with 241MB heap and 64MB offheap memory [pid: 226177] (Linux 6.12.113+ amd64, Eclipse Adoptium 21.0.13 x86_64, MSBDiskFPSet, DiskStateQueue).
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderBug.tla
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderCore.tla
Semantic processing of module OrderCore
Semantic processing of module OrderBug
Starting... (2026-11-11 01:29:10)
Computing initial states...
Finished computing initial states: 1 distinct state generated at 2026-11-11 01:29:10.
Error: Invariant NoUnpaidShipment is violated.
Error: The behavior up to this point is:
State 1: <Initial predicate>
/\ checkedPaid = FALSE
/\ shipPhase = "new"
/\ paid = FALSE

State 2: <Pay line 7, col 8 to line 8, col 62 of module OrderCore>
/\ checkedPaid = FALSE
/\ shipPhase = "new"
/\ paid = TRUE

State 3: <CheckPayment line 9, col 17 to line 11, col 33 of module OrderCore>
/\ checkedPaid = TRUE
/\ shipPhase = "checked"
/\ paid = TRUE

State 4: <Refund line 12, col 11 to line 13, col 66 of module OrderCore>
/\ checkedPaid = TRUE
/\ shipPhase = "checked"
/\ paid = FALSE

State 5: <ShipBug line 14, col 12 to line 15, col 71 of module OrderCore>
/\ checkedPaid = TRUE
/\ shipPhase = "shipped"
/\ paid = FALSE

8 states generated, 6 distinct states found, 1 states left on queue.
The depth of the complete state graph search is 5.
The average outdegree of the complete state graph is 1 (minimum is 1, the maximum 2 and the 95th percentile is 2).
Finished in 00s at (2026-11-11 01:29:10)

TLC实际OS退出码： 12
核验： {"name": "bug", "os_exit_code": 12, "generated": 8, "distinct": 6, "queue": 1, "completed": false, "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"}

```
退出码：0

## 2026-11-11T01:29:11.984560+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine/exercise`

```sh
python3 run_labs.py fixed
```

真实输出：
```text
实际命令： /workspace/learn-batch/03-tla-statemachine/tools/jdk-21.0.13+9-jre/bin/java -Xmx256m -XX:+UseParallelGC -jar /workspace/learn-batch/03-tla-statemachine/tools/tla2tools.jar -workers 1 -fp 0 -config OrderFixed.cfg -metadir /workspace/learn-batch/03-tla-statemachine/exercise/results/fixed-meta -dump dot,actionlabels /workspace/learn-batch/03-tla-statemachine/exercise/results/fixed-graph.dot OrderFixed.tla 
工作目录： /workspace/learn-batch/03-tla-statemachine/exercise/models
TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
Running breadth-first search Model-Checking with fp 0 and seed -1828634581394334619 with 1 worker on 8 cores with 241MB heap and 64MB offheap memory [pid: 226207] (Linux 6.12.113+ amd64, Eclipse Adoptium 21.0.13 x86_64, MSBDiskFPSet, DiskStateQueue).
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderFixed.tla
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderCore.tla
Semantic processing of module OrderCore
Semantic processing of module OrderFixed
Starting... (2026-11-11 01:29:11)
Computing initial states...
Finished computing initial states: 1 distinct state generated at 2026-11-11 01:29:11.
Model checking completed. No error has been found.
  Estimates of the probability that TLC did not check all reachable states
  because two distinct states had the same fingerprint:
  calculated (optimistic):  val = 8.1E-19
8 states generated, 5 distinct states found, 0 states left on queue.
The depth of the complete state graph search is 4.
The average outdegree of the complete state graph is 1 (minimum is 0, the maximum 2 and the 95th percentile is 2).
Finished in 00s at (2026-11-11 01:29:11)

TLC实际OS退出码： 0
核验： {"name": "fixed", "os_exit_code": 0, "generated": 8, "distinct": 5, "queue": 0, "completed": true, "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"}

```
退出码：0

## 2026-11-11T01:29:20.144082+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine/exercise`

```sh
python3 run_labs.py scaling
```

真实输出：
```text
实际命令： /workspace/learn-batch/03-tla-statemachine/tools/jdk-21.0.13+9-jre/bin/java -Xmx256m -XX:+UseParallelGC -jar /workspace/learn-batch/03-tla-statemachine/tools/tla2tools.jar -workers 1 -fp 0 -config Orders1.cfg -metadir /workspace/learn-batch/03-tla-statemachine/exercise/results/orders1-meta -dump dot,actionlabels /workspace/learn-batch/03-tla-statemachine/exercise/results/orders1-graph.dot OrderMany.tla 
工作目录： /workspace/learn-batch/03-tla-statemachine/exercise/models
TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
Running breadth-first search Model-Checking with fp 0 and seed 6709666313448134082 with 1 worker on 8 cores with 241MB heap and 64MB offheap memory [pid: 226304] (Linux 6.12.113+ amd64, Eclipse Adoptium 21.0.13 x86_64, MSBDiskFPSet, DiskStateQueue).
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderMany.tla
Semantic processing of module OrderMany
Starting... (2026-11-11 01:29:18)
Computing initial states...
Finished computing initial states: 1 distinct state generated at 2026-11-11 01:29:18.
Model checking completed. No error has been found.
  Estimates of the probability that TLC did not check all reachable states
  because two distinct states had the same fingerprint:
  calculated (optimistic):  val = 8.1E-19
8 states generated, 5 distinct states found, 0 states left on queue.
The depth of the complete state graph search is 4.
The average outdegree of the complete state graph is 1 (minimum is 0, the maximum 2 and the 95th percentile is 2).
Finished in 00s at (2026-11-11 01:29:18)

TLC实际OS退出码： 0
核验： {"name": "orders1", "os_exit_code": 0, "generated": 8, "distinct": 5, "queue": 0, "completed": true, "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"}
实际命令： /workspace/learn-batch/03-tla-statemachine/tools/jdk-21.0.13+9-jre/bin/java -Xmx256m -XX:+UseParallelGC -jar /workspace/learn-batch/03-tla-statemachine/tools/tla2tools.jar -workers 1 -fp 0 -config Orders2.cfg -metadir /workspace/learn-batch/03-tla-statemachine/exercise/results/orders2-meta -dump dot,actionlabels /workspace/learn-batch/03-tla-statemachine/exercise/results/orders2-graph.dot OrderMany.tla 
工作目录： /workspace/learn-batch/03-tla-statemachine/exercise/models
TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
Running breadth-first search Model-Checking with fp 0 and seed -5137636851064475891 with 1 worker on 8 cores with 241MB heap and 64MB offheap memory [pid: 226335] (Linux 6.12.113+ amd64, Eclipse Adoptium 21.0.13 x86_64, MSBDiskFPSet, DiskStateQueue).
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderMany.tla
Semantic processing of module OrderMany
Starting... (2026-11-11 01:29:18)
Computing initial states...
Finished computing initial states: 1 distinct state generated at 2026-11-11 01:29:18.
Model checking completed. No error has been found.
  Estimates of the probability that TLC did not check all reachable states
  because two distinct states had the same fingerprint:
  calculated (optimistic):  val = 5.0E-17
62 states generated, 25 distinct states found, 0 states left on queue.
The depth of the complete state graph search is 7.
The average outdegree of the complete state graph is 1 (minimum is 0, the maximum 3 and the 95th percentile is 2).
Finished in 00s at (2026-11-11 01:29:19)

TLC实际OS退出码： 0
核验： {"name": "orders2", "os_exit_code": 0, "generated": 62, "distinct": 25, "queue": 0, "completed": true, "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"}
实际命令： /workspace/learn-batch/03-tla-statemachine/tools/jdk-21.0.13+9-jre/bin/java -Xmx256m -XX:+UseParallelGC -jar /workspace/learn-batch/03-tla-statemachine/tools/tla2tools.jar -workers 1 -fp 0 -config Orders3.cfg -metadir /workspace/learn-batch/03-tla-statemachine/exercise/results/orders3-meta -dump dot,actionlabels /workspace/learn-batch/03-tla-statemachine/exercise/results/orders3-graph.dot OrderMany.tla 
工作目录： /workspace/learn-batch/03-tla-statemachine/exercise/models
TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
Running breadth-first search Model-Checking with fp 0 and seed -5754757719060894185 with 1 worker on 8 cores with 241MB heap and 64MB offheap memory [pid: 226378] (Linux 6.12.113+ amd64, Eclipse Adoptium 21.0.13 x86_64, MSBDiskFPSet, DiskStateQueue).
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderMany.tla
Semantic processing of module OrderMany
Starting... (2026-11-11 01:29:19)
Computing initial states...
Finished computing initial states: 1 distinct state generated at 2026-11-11 01:29:19.
Model checking completed. No error has been found.
  Estimates of the probability that TLC did not check all reachable states
  because two distinct states had the same fingerprint:
  calculated (optimistic):  val = 2.2E-15
452 states generated, 125 distinct states found, 0 states left on queue.
The depth of the complete state graph search is 10.
The average outdegree of the complete state graph is 1 (minimum is 0, the maximum 4 and the 95th percentile is 3).
Finished in 00s at (2026-11-11 01:29:19)

TLC实际OS退出码： 0
核验： {"name": "orders3", "os_exit_code": 0, "generated": 452, "distinct": 125, "queue": 0, "completed": true, "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"}

```
退出码：0

## 2026-11-11T01:29:21.058823+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine/exercise`

```sh
python3 run_labs.py mutation
```

真实输出：
```text
实际命令： /workspace/learn-batch/03-tla-statemachine/tools/jdk-21.0.13+9-jre/bin/java -Xmx256m -XX:+UseParallelGC -jar /workspace/learn-batch/03-tla-statemachine/tools/tla2tools.jar -workers 1 -fp 0 -config OrderMutant.cfg -metadir /workspace/learn-batch/03-tla-statemachine/exercise/results/mutant-meta -dump dot,actionlabels /workspace/learn-batch/03-tla-statemachine/exercise/results/mutant-graph.dot OrderMutant.tla 
工作目录： /workspace/learn-batch/03-tla-statemachine/exercise/models
TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
Running breadth-first search Model-Checking with fp 0 and seed -2945173793223592271 with 1 worker on 8 cores with 241MB heap and 64MB offheap memory [pid: 226407] (Linux 6.12.113+ amd64, Eclipse Adoptium 21.0.13 x86_64, MSBDiskFPSet, DiskStateQueue).
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderMutant.tla
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderCore.tla
Semantic processing of module OrderCore
Semantic processing of module OrderMutant
Starting... (2026-11-11 01:29:20)
Computing initial states...
Finished computing initial states: 1 distinct state generated at 2026-11-11 01:29:20.
Error: Invariant NoUnpaidShipment is violated.
Error: The behavior up to this point is:
State 1: <Initial predicate>
/\ checkedPaid = FALSE
/\ shipPhase = "new"
/\ paid = FALSE

State 2: <Pay line 7, col 8 to line 8, col 62 of module OrderCore>
/\ checkedPaid = FALSE
/\ shipPhase = "new"
/\ paid = TRUE

State 3: <CheckPayment line 9, col 17 to line 11, col 33 of module OrderCore>
/\ checkedPaid = TRUE
/\ shipPhase = "checked"
/\ paid = TRUE

State 4: <Refund line 12, col 11 to line 13, col 66 of module OrderCore>
/\ checkedPaid = TRUE
/\ shipPhase = "checked"
/\ paid = FALSE

State 5: <ShipBug line 14, col 12 to line 15, col 71 of module OrderCore>
/\ checkedPaid = TRUE
/\ shipPhase = "shipped"
/\ paid = FALSE

8 states generated, 6 distinct states found, 1 states left on queue.
The depth of the complete state graph search is 5.
The average outdegree of the complete state graph is 1 (minimum is 1, the maximum 2 and the 95th percentile is 2).
Finished in 00s at (2026-11-11 01:29:20)

TLC实际OS退出码： 12
核验： {"name": "mutant", "os_exit_code": 12, "generated": 8, "distinct": 6, "queue": 1, "completed": false, "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"}

```
退出码：0

## 2026-11-11T01:29:21.136654+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine/exercise`

```sh
python3 run_labs.py replay
```

真实输出：
```text
{
  "trace_actions": [
    "Pay",
    "CheckPayment",
    "Refund",
    "ShipBug"
  ],
  "states": [
    {
      "paid": false,
      "shipPhase": "new",
      "checkedPaid": false
    },
    {
      "paid": true,
      "shipPhase": "new",
      "checkedPaid": false
    },
    {
      "paid": true,
      "shipPhase": "checked",
      "checkedPaid": true
    },
    {
      "paid": false,
      "shipPhase": "checked",
      "checkedPaid": true
    },
    {
      "paid": false,
      "shipPhase": "shipped",
      "checkedPaid": true
    }
  ],
  "transition_count": 4,
  "state_count": 5,
  "python_fixed_reachable": 5,
  "python_bug_full_reachable": 6,
  "fixed_TLC_DOT_equals_python_full_state_set": true,
  "fixed_blocks_bug_final_transition": true,
  "scope": "仅自编合成实现的逐步重放与状态集合交叉检查；非产品代码精化证明"
}

```
退出码：0

## 2026-11-11T01:30:36.551343+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine`

```sh
python3 exercise/setup_tools.py
```

真实输出：
```text
openjdk version "21.0.13" 2026-10-20 LTS
OpenJDK Runtime Environment Temurin-21.0.13+9 (build 21.0.13+9-LTS)
OpenJDK 64-Bit Server VM Temurin-21.0.13+9 (build 21.0.13+9-LTS, mixed mode, sharing)
SHA256匹配 OpenJDK21U-jre_x64_linux_hotspot_21.0.13_9.tar.gz a535a1df9c6284d9618872984e026ae0352d1f7e9e0605425c0e6114f47351dd
SHA256匹配 tla2tools.jar 936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88
TLC release发布正文SHA1也匹配；SHA1不是签名认证。
Java只在 /workspace/learn-batch/03-tla-statemachine/tools/jdk-21.0.13+9-jre/bin/java

```
退出码：0

## 2026-11-11T01:30:36.622603+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine`

```sh
python3 -m py_compile exercise/order_reference.py exercise/run_labs.py
```

真实输出：
```text

```
退出码：0

## 2026-11-11T01:30:37.564253+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine/exercise`

```sh
python3 run_labs.py fixed
```

真实输出：
```text
实际命令： /workspace/learn-batch/03-tla-statemachine/tools/jdk-21.0.13+9-jre/bin/java -Xmx256m -XX:+UseParallelGC -jar /workspace/learn-batch/03-tla-statemachine/tools/tla2tools.jar -workers 1 -fp 0 -config OrderFixed.cfg -metadir /workspace/learn-batch/03-tla-statemachine/exercise/results/fixed-meta -dump dot,actionlabels /workspace/learn-batch/03-tla-statemachine/exercise/results/fixed-graph.dot OrderFixed.tla 
工作目录： /workspace/learn-batch/03-tla-statemachine/exercise/models
TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
Running breadth-first search Model-Checking with fp 0 and seed 1178003649751502381 with 1 worker on 8 cores with 241MB heap and 64MB offheap memory [pid: 228631] (Linux 6.12.113+ amd64, Eclipse Adoptium 21.0.13 x86_64, MSBDiskFPSet, DiskStateQueue).
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderFixed.tla
Parsing file /workspace/learn-batch/03-tla-statemachine/exercise/models/OrderCore.tla
Semantic processing of module OrderCore
Semantic processing of module OrderFixed
Starting... (2026-11-11 01:30:37)
Computing initial states...
Finished computing initial states: 1 distinct state generated at 2026-11-11 01:30:37.
Model checking completed. No error has been found.
  Estimates of the probability that TLC did not check all reachable states
  because two distinct states had the same fingerprint:
  calculated (optimistic):  val = 8.1E-19
8 states generated, 5 distinct states found, 0 states left on queue.
The depth of the complete state graph search is 4.
The average outdegree of the complete state graph is 1 (minimum is 0, the maximum 2 and the 95th percentile is 2).
Finished in 00s at (2026-11-11 01:30:37)

TLC实际OS退出码： 0
核验： {"name": "fixed", "os_exit_code": 0, "generated": 8, "distinct": 5, "queue": 0, "completed": true, "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"}

```
退出码：0

## 2026-11-11T01:34:06.747154+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine`

```sh
python3 _tools/render_pdf.py 'TLA状态机-从反例到修复.html' 'TLA状态机-从反例到修复.pdf'
```

真实输出：
```text
命令： ['/opt/google/chrome/chrome', '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--timeout=15000', '--no-pdf-header-footer', '--disable-background-networking', '--user-data-dir=/workspace/learn-batch/03-tla-statemachine/render-profile', '--print-to-pdf=/workspace/learn-batch/03-tla-statemachine/TLA状态机-从反例到修复.pdf', 'file:///workspace/learn-batch/03-tla-statemachine/TLA%E7%8A%B6%E6%80%81%E6%9C%BA-%E4%BB%8E%E5%8F%8D%E4%BE%8B%E5%88%B0%E4%BF%AE%E5%A4%8D.html']
[1111/013321.754160:WARNING:chrome/app/chrome_main_linux.cc:84] Read channel stable from /opt/google/chrome/CHROME_VERSION_EXTRA
[233498:233520:1111/013321.795561:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[233498:233520:1111/013321.822473:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[233498:233520:1111/013321.822533:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[233498:233520:1111/013321.822894:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[233498:233520:1111/013321.978700:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[233498:233520:1111/013321.978738:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[233498:233498:1111/013321.990208:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.Properties.GetAll: object_path= /org/freedesktop/UPower/devices/DisplayDevice: unknown error type: 
Created TensorFlow Lite XNNPACK delegate for CPU.
Traceback (most recent call last):
  File "/workspace/learn-batch/03-tla-statemachine/_tools/render_pdf.py", line 7, in <module>
    print('命令：',cmd,flush=True);r=subprocess.run(cmd,timeout=45,env={**os.environ,'FONTCONFIG_FILE':'/etc/fonts/fonts.conf','FONTCONFIG_PATH':'/etc/fonts'});raise SystemExit(r.returncode)
                                     ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 556, in run
    stdout, stderr = process.communicate(input, timeout=timeout)
                     ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1222, in communicate
    stdout, stderr = self._communicate(input, endtime, timeout)
                     ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 2154, in _communicate
    self.wait(timeout=self._remaining_time(endtime))
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1280, in wait
    return self._wait(timeout=timeout)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 2058, in _wait
    raise TimeoutExpired(self.args, timeout)
subprocess.TimeoutExpired: Command '['/opt/google/chrome/chrome', '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--timeout=15000', '--no-pdf-header-footer', '--disable-background-networking', '--user-data-dir=/workspace/learn-batch/03-tla-statemachine/render-profile', '--print-to-pdf=/workspace/learn-batch/03-tla-statemachine/TLA状态机-从反例到修复.pdf', 'file:///workspace/learn-batch/03-tla-statemachine/TLA%E7%8A%B6%E6%80%81%E6%9C%BA-%E4%BB%8E%E5%8F%8D%E4%BE%8B%E5%88%B0%E4%BF%AE%E5%A4%8D.html']' timed out after 45 seconds

```
退出码：1

## 2026-11-11T01:34:20.744004+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine`

```sh
python3 _tools/render_pdf.py 'TLA状态机-从反例到修复.html' 'TLA状态机-从反例到修复.pdf'
```

真实输出：
```text
命令： ['/opt/google/chrome/chrome', '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--timeout=15000', '--no-pdf-header-footer', '--disable-background-networking', '--user-data-dir=/workspace/learn-batch/03-tla-statemachine/render-profile', '--print-to-pdf=/workspace/learn-batch/03-tla-statemachine/TLA状态机-从反例到修复.pdf', 'file:///workspace/learn-batch/03-tla-statemachine/TLA%E7%8A%B6%E6%80%81%E6%9C%BA-%E4%BB%8E%E5%8F%8D%E4%BE%8B%E5%88%B0%E4%BF%AE%E5%A4%8D.html']
[1111/013419.718326:WARNING:chrome/app/chrome_main_linux.cc:84] Read channel stable from /opt/google/chrome/CHROME_VERSION_EXTRA
[234629:234650:1111/013419.762992:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[234629:234650:1111/013419.795196:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[234629:234650:1111/013419.795467:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[234629:234650:1111/013419.795578:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[234629:234650:1111/013419.954673:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[234629:234650:1111/013419.954706:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[234629:234629:1111/013419.964793:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.Properties.GetAll: object_path= /org/freedesktop/UPower/devices/DisplayDevice: unknown error type: 
Created TensorFlow Lite XNNPACK delegate for CPU.
1061383 bytes written to file /workspace/learn-batch/03-tla-statemachine/TLA状态机-从反例到修复.pdf

```
退出码：0

## 最终判读
- TLC帮助命令-help退出1为显示帮助的行为，不是模型检查失败。
- bug/mutant的真实TLC退出12；驱动识别到预期性质违反才返回0，不将它们标成模型通过。fixed与1/2/3订单边界分别退出0，队列0。
- pstack官方提交时间换算为2026-11-10 11:28:06 Asia/Shanghai；镜像发现提交时间换算2026-11-10 20:35:58 Asia/Shanghai。
- PDF首次45秒超时后，同一默认沙箱打印命令原样重试成功，12页A4已逐页pdftoppm并Read检查。构建指南脚本最初仅有Python反斜线SyntaxWarning，已修正转义后重新生成、打印和检查，不影响TLA模型。
- 没有安装/调用pstack插件、付费API、真实支付、账号、密钥、日程、发布、push、公开仓库修改或安全设置变更；未更改其他助手目录。

## 2026-11-11T01:38:21.964429+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine`

```sh
python3 _tools/validate_artifacts.py
```

真实输出：
```text
{
  "访问日期": "2026-11-11 Asia/Shanghai",
  "问答": 12,
  "内联SVG": 13,
  "用途": 5,
  "主实验步骤": 6,
  "PDF页数": 12,
  "逐页Read检查": 12,
  "PDF文本字符数": 11051,
  "替换字符": 0,
  "案例汇总": {
    "bug": {
      "name": "bug",
      "os_exit_code": 12,
      "generated": 8,
      "distinct": 6,
      "queue": 1,
      "completed": false,
      "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"
    },
    "fixed": {
      "name": "fixed",
      "os_exit_code": 0,
      "generated": 8,
      "distinct": 5,
      "queue": 0,
      "completed": true,
      "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"
    },
    "orders1": {
      "name": "orders1",
      "os_exit_code": 0,
      "generated": 8,
      "distinct": 5,
      "queue": 0,
      "completed": true,
      "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"
    },
    "orders2": {
      "name": "orders2",
      "os_exit_code": 0,
      "generated": 62,
      "distinct": 25,
      "queue": 0,
      "completed": true,
      "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"
    },
    "orders3": {
      "name": "orders3",
      "os_exit_code": 0,
      "generated": 452,
      "distinct": 125,
      "queue": 0,
      "completed": true,
      "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"
    },
    "mutant": {
      "name": "mutant",
      "os_exit_code": 12,
      "generated": 8,
      "distinct": 6,
      "queue": 1,
      "completed": false,
      "meaning": "TLC有限模型检查；非任意规模证明或真实支付产品验收"
    }
  },
  "TLC反例状态数": 5,
  "TLC反例转移数": 4,
  "不变量配置保持一致": true,
  "覆盖文件基线哈希匹配": true,
  "证据边界": "合成订单有限模型；不是真实支付产品、活性或任意规模证明"
}

```
退出码：0

## 2026-11-11T01:38:22.331086+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine`

```sh
git ls-remote https://github.com/Smashwinny/reminder_knowlege refs/heads/main
```

真实输出：
```text
a8674777e18302b8804b137212b1396cbfe5a747	refs/heads/main

```
退出码：0

## 2026-11-11T01:38:23.001545+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/03-tla-statemachine`

```sh
git ls-remote https://github.com/cursor/plugins refs/heads/main
```

真实输出：
```text
de8ee15dd1194627d21eb5fcd41cb1873208dabb	refs/heads/main

```
退出码：0

## ZIP真实验收
执行 `python3 _tools/package_deliverables.py`；练习ZIP 47条目CRC全部通过。实际解压到本项package-smoke后，指定本项Java/JAR，运行 `python3 run_labs.py bug`、`fixed`、`replay`，驱动均退出0（bug内部TLC仍真实退出12）。完整实际命令/输出见portable-smoke.log，不混作新增的主实验案例。
