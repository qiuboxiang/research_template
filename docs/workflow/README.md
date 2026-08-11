# 科研工作流

## 1. 初始化投稿目标

投稿目标由 Codex 按
[`paper/target/venue-research.prompt.md`](../../paper/target/venue-research.prompt.md)
主动联网检索并交叉核对；`researchctl` 负责规则解析、Schema 校验、ZIP 安全检查和
内容哈希，不把正则解析结果当作唯一事实来源。可以直接告诉 Codex：

> 按 venue research prompt 初始化/刷新当前投稿目标并安装经过验证的官方模板。

```bash
researchctl init --target iclr-2027
researchctl venue sync
researchctl venue status
```

会议规则写入 `paper/target/venue.yaml`。若官方模板尚不可用，状态会保持为
`awaiting_official_template`，系统不会自动采用上一年度模板。

## 2. 登记数据

```bash
researchctl data register \
  --name synthetic-regression --version 1.0.0 \
  --source generated://synthetic --license CC0-1.0 \
  --split train=sha256:demo-train --split test=sha256:demo-test \
  --preprocessing "Deterministic linear samples"
```

实体数据放在 `artifacts/data/` 并由 DVC 管理；Git 只保存注册表和 `.dvc`
指针。

## 3. 运行训练和评测

```bash
researchctl run train --config configs/experiment/synthetic.yaml
researchctl eval run --checkpoint-id 'ckpt:<run>/best-<hash>' \
  --dataset-id 'dataset:synthetic-regression@1.0.0'
```

训练会归档 resolved config、seed、Git SHA/dirty patch、环境、MLflow ID、
checkpoint hash 和指标。Slurm 使用 `configs/launcher/slurm.yaml`；多卡运行使用
`torchrun --nproc-per-node=<N> ...` 启动同一个入口。

## 4. 关联论文证据

```bash
researchctl paper link \
  --label fig:main \
  --kind figure \
  --source artifacts/evals/<file> \
  --run-id '<run-id>' --eval-id '<eval-id>'
```

命令将文件复制到 `paper/generated/`，记录 SHA256，并刷新候选 release。

## 5. Overleaf

在 Overleaf 创建空白 Premium 项目后：

```bash
researchctl paper bootstrap-overleaf --project-id PROJECT_ID
researchctl paper pull
researchctl paper push-generated
```

token 交给 Git credential helper，绝不写入配置。论文正文以 Overleaf 为准；
若本地和远端同时修改同一文件，pull 会停止并输出冲突报告。

## 6. Release

```bash
researchctl release refresh
researchctl release check --strict
researchctl release freeze --version v1.0.0
researchctl release anonymize --version v1.0.0
researchctl release publish --version v1.0.0 --dry-run
```

`releases/current.yaml` 只选择 `paper/evidence.yaml` 可达的实验、数据、评测和
checkpoint；尚未被论文引用的记录列在 `unlinked`，不会混入正式发布。

最终执行外部发布时需要去掉 `--dry-run` 并添加 `--confirm`。不能再分发的
数据只发布数据卡、来源、构建脚本和校验和。
