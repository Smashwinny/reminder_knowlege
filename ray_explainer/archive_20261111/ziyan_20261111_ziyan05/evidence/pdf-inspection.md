# A4 PDF逐页Read自检

2026-11-11 Asia/Shanghai；WeasyPrint 70.0实际渲染，pdfinfo确认12页、595.276×841.89pt。pdftoppm -scale-to 1300 -png逐页生成PNG，全部12页均通过Read单独查看；不是独立审核。

|页|PNG|观察|SHA256|
|---|---|---|---|
|1|page-01.png|封面与大号重点完整，SHA可读|5dc659b40a1961d86f4391c7a6c1211509f3a5ce1ad20756c3a77348153e8e33|
|2|page-02.png|Q01/02文字、SVG无截断|d515341caf9fa05c741f900f4e90a7141801ca80d716151e19ee566af2d8101c|
|3|page-03.png|Q03/04文字、SVG无截断|0271878b339e4237a0b0d826eade130e2deeefe61bf7d151a85b71a40d902b27|
|4|page-04.png|Q05/06文字、SVG无截断|0efaa7a27c31d52997f3a9c08052886120cc3c6fa45b42bfdebc6ba960b9479a|
|5|page-05.png|Q07/08文字、SVG无截断|3b63f5c35193449050f77f35ee395b445ab8d1e3e60bc6e1f41712299705b3c6|
|6|page-06.png|Q09/10失败门禁与0.35秒差异可读|f56432cb5d6493773cdf8d6e351a2d54ad644e1feac69255e7702ae203017bc5|
|7|page-07.png|Q11/12字体边界与许可完整|48c00a9bf179a81a36d67edcce0c91ebaa1547815d90ec5c3b860f4bfa5254dd|
|8|page-08.png|4种用途及文件契约完整|82645611e015fbe9da28c9c03460eb334d9c6c54dcb543d96faf7cf1c615a2d4|
|9|page-09.png|步骤1–2命令块、结果与验证完整|f1164dd0cbac1a378d6f941b0c2afa5705cb68a0d30a8928984c09a53f473b1c|
|10|page-10.png|步骤3–4命令块、结果与验证完整|07d518c3365147544ca9724d093826449d39606e38a9a5f8aaab53211c947373|
|11|page-11.png|步骤5–6长命令自动折行，无越界，底部验证仍可读|2180d619fcac0838a8586198cfe5f33f6aacdecce766282cec5a8847c3f09eee|
|12|page-12.png|3幕小图可读、状态表完整，无横向裁切|03f16e3176f11002dcbf609b28815cf093bdc8f0511ef0fc788a5a33a7747768|
