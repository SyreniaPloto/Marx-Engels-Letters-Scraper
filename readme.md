# Marx Engels Letters Scraper

![CI](https://github.com//marx_engels_letters_scraper/actions/workflows/ci.yml/badge.svg)

## Overview 概述
This project scrapes letters from the Marx Engels digital archive and verifies the completeness and correctness of the data.

本项目从马克思恩格斯数字档案中爬取信件，并验证数据的完整性和正确性。

## Features 特性

- **Multi-threaded scraping**: Efficiently scrapes letters using multiple threads.
- **Progress tracking**: Automatically saves progress and retries failed requests.
- **Data validation**: Verifies the completeness and correctness of the scraped data.
- **Temporary file cleanup**: Cleans up temporary files after successful scraping.

- **多线程爬取**：使用多线程高效地爬取信件。
- **进度跟踪**：自动保存进度并重试失败的请求。
- **数据验证**：验证爬取数据的完整性和正确性。
- **临时文件清理**：成功爬取后清理临时文件。

## Installation 安装
```bash
git clone https://github.com/SyreniaPloto/Marx-Engels-Letters-Scraper.git
cd marx_engels_letters_scraper
pip install -r requirements.txt
```

## Usage 使用方法
To start scraping and verifying the data, run:
要开始爬取和验证数据，请运行：
```bash
python main.py
```

To only verify the data, run:
仅验证数据，请运行：

```bash
python verifier.py
```

## License and Attribution 许可和归属
This project is licensed under the MIT License. See the LICENSE file for details.

本项目基于 MIT 许可证。有关详细信息，请参阅 LICENSE 文件。

This project uses data from the Marx-Engels-Gesamtausgabe (MEGA2) digital archive, which is shared under the [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.zh-hans) license.

本项目使用的数据来自马克思恩格斯全集 (MEGA2) 数字档案，依据 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.zh-hans) 许可证 共享。

Original data source: [Marx-Engels-Gesamtausgabe (MEGA2) digital archive](https://megadigital.bbaw.de/briefe/index.xql?&offset=1)

数据来源：[马克思恩格斯全集 (MEGA2) 数字档案](https://megadigital.bbaw.de/briefe/index.xql?&offset=1)

## Contributing 贡献
Contributions are welcome! Please open an issue or submit a pull request.

欢迎贡献！请提出 issue 或提交 pull request。