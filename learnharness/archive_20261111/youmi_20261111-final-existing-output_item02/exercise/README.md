# LearnHarness 原始纯模块实验
Node24.22.1实跑；官方建议Node26。零API、零npm依赖；原模块不改。
```bash
node exercise/lab.mjs extract
node exercise/lab.mjs manifest
node --test exercise/upstream-pure.test.ts
node exercise/lab.mjs positive
node exercise/lab.mjs negative
node exercise/lab.mjs selftest
```
自写runner与选定上游纯测试不等于完整官方套件。AGPL原模块、原测试及LICENSE见upstream；来源固定SHA见sources.md。
