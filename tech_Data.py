from neo4j import GraphDatabase


class Date:
    def __init__(self):
        # 反应类型
        self.Action = [
            {"id": "action_001", "name": "物理过程", "description": "物理气相沉积"},
            {"id": "action_002", "name": "化学过程", "description": "化学气相沉积"},
            {"id": "action_003", "name": "电化学过程", "description": "通过电化学反应沉积薄膜"},
            {"id": "action_004", "name": "热过程", "description": "通过热能驱动反应沉积薄膜"},
            {"id": "action_005", "name": "等离子体过程", "description": "利用等离子体增强反应过程"},


        ]
        # 技术大类节点数据
        self.Technology = [
            {"id": "tech_001", "name": "PVD", "description": "通过物理方法使材料气化并在基片上沉积成膜的技术，主要包括溅射、蒸镀、离子镀和脉冲激光沉积（PLD）"},
            {"id": "tech_002", "name": "CVD", "description": "通过气态前驱体在基片表面发生化学反应生成固态薄膜的技术"},
            {"id": "tech_003", "name": "ALD", "description": "通过交替通入不同的前驱体，在基片表面逐层自限制反应生长薄膜，具有极好的均匀性和台阶覆盖性"},
            {"id": "tech_004", "name": "溶液法", "description": "通过溶液状态的材料在基片上成膜，适用于大面积、柔性、低成本制备"},
            {"id": "tech_005", "name": "外延生长", "description": "在单晶基片上生长具有特定晶向的单晶薄膜的技术"},
            {"id": "tech_006", "name": "3D集成技术", "description": "通过硅通孔(TSV)等技术实现芯片垂直堆叠的先进封装技术"},
            {"id": "tech_007", "name": "异质集成", "description": "将不同材料体系的器件集成在同一芯片上的技术"},
            {"id": "tech_008", "name": "量子器件制造", "description": "用于制造量子比特和量子计算器件的特殊工艺技术"},
            {"id": "tech_009", "name": "电化学沉积技术", "description": "通过电化学反应在基片上沉积金属或半导体薄膜"},
            {"id": "tech_010", "name": "等离子体技术", "description": "利用等离子体增强沉积、刻蚀或表面处理的技术"},
            {"id": "tech_011", "name": "激光加工技术", "description": "利用激光进行沉积、退火、刻蚀等加工的技术"},
            {"id": "tech_012", "name": "纳米压印技术", "description": "通过模板进行纳米级图案转移的技术"},
            {"id": "tech_013", "name": "自组装技术", "description": "利用分子或纳米粒子自组装形成有序结构的技术"},
            {"id": "tech_014", "name": "混合沉积技术", "description": "结合多种沉积方法的复合技术"},
            {"id": "tech_015", "name": "智能沉积技术", "description": "集成AI和机器学习优化的沉积工艺"},
            {"id": "tech_016", "name": "神经形态计算制造", "description": "制造模拟人脑计算模式的神经形态芯片的技术"},
            {"id": "tech_017", "name": "生物电子集成", "description": "将生物元件与电子器件集成的技术"},
            {"id": "tech_018", "name": "可持续绿色制造", "description": "环境友好、低能耗的半导体制造技术"},
            {"id": "tech_019", "name": "极端环境电子制造", "description": "制造能在高温、辐射等极端环境下工作的电子器件"},
            {"id": "tech_020", "name": "光子集成制造", "description": "制造集成光子器件的技术"},
        
            {"id": "tech_021", "name": "物理气相沉积", "description": "在真空环境中，通过物理方式（如蒸发、溅射）将固体源材料转化为气态，再凝结在衬底表面形成薄膜。"},
            {"id": "tech_022", "name": "化学气相沉积", "description": "通过气态前驱体在衬底表面发生化学反应，生成固态薄膜并副产物排出。能实现高度共形、均匀的薄膜沉积。"},
            {"id": "tech_023", "name": "原子层沉积", "description": "化学气相沉积的进阶形式，通过在表面依次发生自限制性化学反应，能实现亚纳米级的厚度控制和极致共形性。"},]

        # 方法节点数据
        self.Method = [
            # PVD 方法
            {"id": "method_001", "name": "溅射", "description": "利用等离子体轰击靶材，使靶材原子或分子溅射出来并沉积在基片表面形成薄膜"},
            {"id": "method_002", "name": "蒸镀", "description": "通过加热使材料蒸发或升华，气态物质在基片表面冷凝成膜"},
            {"id": "method_003", "name": "离子镀", "description": "结合蒸发和等离子体离化技术，蒸发出的材料原子被离子化后在电场作用下加速沉积，附着力强、膜层致密"},
            {"id": "method_004", "name": "PLD", "description": "使用高能脉冲激光轰击靶材，使其瞬间气化并在基片上沉积成膜，适用于复杂组分材料的制备"},
            {"id": "method_026", "name": "IBAD", "description": "离子束辅助沉积，结合蒸发和离子束轰击，改善薄膜质量"},
            {"id": "method_027", "name": "ECR-PVD", "description": "电子回旋共振物理气相沉积，高离化率的PVD技术"},
            # CVD 方法
            {"id": "method_005", "name": "PECVD", "description": "利用等离子体活化反应前驱体，降低反应温度，提高沉积速率和薄膜质量"},
            {"id": "method_006", "name": "MOCVD", "description": "使用金属有机化合物作为前驱体，适用于Ⅲ-Ⅴ族、Ⅱ-Ⅵ族化合物半导体薄膜的生长。"},
            {"id": "method_007", "name": "APCVD", "description": "在常压下进行，反应速度快，设备简单，但均匀性和台阶覆盖性较差"},
            {"id": "method_008", "name": "LPCVD", "description": "在低压下进行，反应均匀性好，台阶覆盖性优，通常为高温过程，适用于高质量薄膜制备"},
            {"id": "method_022", "name": "SACVD", "description": "亚常压化学气相沉积，用于高深宽比间隙填充"},
            {"id": "method_023", "name": "ECR-CVD", "description": "电子回旋共振化学气相沉积，高密度等离子体，低温沉积"},
            {"id": "method_024", "name": "HWCVD", "description": "热丝化学气相沉积，通过热丝分解气体，用于金刚石和硅薄膜"},
            {"id": "method_025", "name": "Cat-CVD", "description": "催化化学气相沉积，类似热丝CVD但使用催化金属丝"},
            # ALD 方法
            {"id": "method_009", "name": "热ALD", "description": "依靠热能驱动表面反应，对器件损伤小，适用于敏感器件和低温工艺"},
            {"id": "method_010", "name": "PE-ALD", "description": "利用等离子体活化一种反应前驱体，降低反应温度，提高反应效率，适用于低温高质量成膜"},
            # 溶液法方法
            {"id": "method_011", "name": "旋涂", "description": "将溶液滴在基片上高速旋转，通过离心力形成均匀薄膜"},
            {"id": "method_012", "name": "喷墨打印", "description": "通过喷头将溶液以液滴形式精确打印在基片上，图案化能力强"},
            {"id": "method_013", "name": "狭缝涂布", "description": "通过狭缝挤出溶液，在移动的基片上形成连续均匀的湿膜"},
            {"id": "method_014", "name": "Langmuir-Blodgett", "description": "通过Langmuir-Blodgett槽将单分子层从液面转移至基片，可制备超薄膜"},
            {"id": "method_015", "name": "电化学沉积", "description": "通过电化学反应在导电基片上沉积金属或半导体薄膜"},
            {"id": "method_016", "name": "水热/溶剂热法", "description": "在高温高压的密闭容器中通过溶液反应合成晶体或薄膜"},
            {"id": "method_017", "name": "凹版印刷", "description": "通过凹版滚筒将图案转移到基片上，适用于连续卷对卷工艺"},
            {"id": "method_018", "name": "丝网印刷", "description": "通过丝网模板将浆料印刷在基片上，适用于厚膜制备"},
            {"id": "method_028", "name": "溶胶-凝胶法", "description": "通过溶液中的溶胶-凝胶转变制备氧化物薄膜"},
            {"id": "method_029", "name": "电纺丝", "description": "通过高压静电力制备纳米纤维薄膜"},
            {"id": "method_030", "name": "分子自组装", "description": "通过分子间作用力自发形成有序结构"},
            # 外延生长方法
            {"id": "method_019", "name": "MBE", "description": "分子束外延，在超高真空环境下，通过分子束源在基片表面逐层外延生长，控制精度高，适用于高质量半导体器件"},
            {"id": "method_020", "name": "LPE", "description": "液相外延，通过熔融液在基片表面冷却析出晶体，设备简单，适用于某些化合物半导体"},
            {"id": "method_021", "name": "VPE", "description": "气相外延，通过气相反应在基片表面外延生长薄膜，包括HVPE（卤化物气相外延）等变体"},

            {"id": "method_031", "name": "喷雾热解", "description": "通过雾化前驱体溶液并在加热基片上反应形成薄膜"},
            {"id": "method_032", "name": "原子层刻蚀", "description": "ALE，与ALD类似的逐层刻蚀技术，实现原子级精度刻蚀"},
            {"id": "method_033", "name": "选择性地沉积", "description": "仅在特定区域沉积材料，减少光刻步骤"},
            {"id": "method_034", "name": "区域选择性ALD", "description": "利用表面化学差异实现选择性沉积"},
            {"id": "method_035", "name": "分子层沉积", "description": "MLD，类似于ALD但用于有机聚合物薄膜"},

            {"id": "method_036", "name": "TSV填充", "description": "硅通孔填充技术，用于3D集成"},
            {"id": "method_037", "name": "晶圆键合", "description": "将两片晶圆永久或临时键合的技术"},
            {"id": "method_038", "name": "选择性外延", "description": "仅在特定区域进行外延生长的技术"},
            {"id": "method_039", "name": "纳米压印", "description": "使用模板进行纳米级图案转移的技术"},
            {"id": "method_040", "name": "定向自组装", "description": "DSA，利用嵌段共聚物自组装形成纳米图案"},
            {"id": "method_041", "name": "原子级抛光", "description": "实现原子级平整表面的抛光技术"},
            {"id": "method_042", "name": "激光退火", "description": "使用激光进行局部退火，改善材料特性"},
            {"id": "method_043", "name": "离子注入", "description": "通过离子轰击改变材料掺杂浓度的技术"},
            {"id": "method_044", "name": "等离子体处理", "description": "使用等离子体进行表面改性或清洗"},
            {"id": "method_045", "name": "激光化学气相沉积", "description": "LCVD，利用激光局部加热实现选择性沉积"},
            {"id": "method_046", "name": "电子束诱导沉积", "description": "EBID，利用电子束分解前驱体实现纳米级沉积"},
            {"id": "method_047", "name": "离子束沉积", "description": "IBD，利用离子束直接沉积薄膜"},
            {"id": "method_048", "name": "团簇束沉积", "description": "CBD，利用原子团簇沉积薄膜，减少缺陷"},
            {"id": "method_049", "name": "气相外延-原子层沉积复合技术", "description": "VPE-ALD，结合VPE和ALD的优势"},
            {"id": "method_050", "name": "等离子体增强脉冲激光沉积", "description": "PE-PLD，结合等离子体增强的PLD技术"},
            {"id": "method_051", "name": "热纳米压印", "description": "在加热条件下进行的纳米压印工艺"},
            {"id": "method_052", "name": "紫外纳米压印", "description": "利用紫外光固化树脂的纳米压印工艺"},
            {"id": "method_053", "name": "软纳米压印", "description": "使用软模板的纳米压印技术"},

            # 自组装相关
            {"id": "method_054", "name": "嵌段共聚物自组装", "description": "利用嵌段共聚物相分离形成纳米图案"},
            {"id": "method_055", "name": "DNA引导自组装", "description": "利用DNA分子进行精确的纳米组装"},
            {"id": "method_056", "name": "胶体晶体自组装", "description": "通过胶体粒子自组装形成光子晶体"},

            # 混合技术
            {"id": "method_057", "name": "PVD-CVD复合沉积", "description": "结合PVD和CVD的混合沉积技术"},
            {"id": "method_058", "name": "电化学-ALD复合技术", "description": "结合电化学沉积和ALD的技术"},
            {"id": "method_059", "name": "激光-溶液复合沉积", "description": "结合激光处理和溶液法的沉积技术"},

            # 智能技术
            {"id": "method_060", "name": "AI优化沉积", "description": "利用人工智能算法优化沉积参数"},
            {"id": "method_061", "name": "实时过程控制", "description": "基于传感器数据的实时工艺控制"},
            {"id": "method_062", "name": "数字孪生沉积", "description": "基于数字孪生技术的沉积过程模拟和优化"},
            {"id": "method_063", "name": "RCA清洗", "description": "半导体标准湿法清洗流程，用于去除有机/无机污染物"},
            {"id": "method_064", "name": "等离子体表面活化", "description": "沉积前通过等离子体处理活化表面，提升后续薄膜附着力"},
            {"id": "method_065", "name": "热ALD工艺", "description": "采用热驱动ALD在衬底表面逐层生长薄膜，常用于高k栅介质沉积"},

        
            {"id": "method_066", "name": "蒸发", "description": "物理气相沉积中的一种物理方式。"},]

        # 子方法节点数据
        self.SubMethod = [
            {"id": "submethod_001", "name": "直流溅射", "description": "适用于导电靶材，通过直流电源产生等离子体"},
            {"id": "submethod_002", "name": "射频溅射", "description": "适用于非导电靶材，通过射频电源激发等离子体"},
            {"id": "submethod_003", "name": "磁控溅射", "description": "引入磁场增强等离子体密度，提高沉积速率和薄膜质量"},
            {"id": "submethod_004", "name": "电子束蒸发", "description": "利用电子束轰击材料局部加热，适用于高熔点材料"},
            {"id": "submethod_005", "name": "热蒸发", "description": "通过电阻加热或感应加热使材料蒸发，简单易控，适用于低熔点材料"},
            {"id": "submethod_006", "name": "反应溅射", "description": "在溅射过程中引入反应气体，沉积化合物薄膜"},
            {"id": "submethod_007", "name": "共溅射", "description": "同时使用多个靶材，制备合金或复合薄膜"},
            {"id": "submethod_008", "name": "高功率脉冲磁控溅射", "description": "HIPIMS，高离化率的溅射技术，改善薄膜质量"},
            {"id": "submethod_009", "name": "激光辅助CVD", "description": "使用激光局部加热或光解，实现选区沉积"},
            {"id": "submethod_010", "name": "原子层刻蚀", "description": "ALE，与ALD类似的逐层刻蚀技术，高精度刻蚀"},
            {"id": "submethod_011", "name": "等离子体增强溅射", "description": "结合等离子体增强的溅射技术"},
            {"id": "submethod_012", "name": "激光辅助ALD", "description": "利用激光增强的原子层沉积"},
            {"id": "submethod_013", "name": "磁场辅助沉积", "description": "在外加磁场条件下进行沉积"},
            {"id": "submethod_014", "name": "超声辅助沉积", "description": "利用超声波增强沉积过程"},
            {"id": "submethod_015", "name": "氢氟酸（HF）漂洗", "description": "使用氢氟酸去除晶圆表面自然氧化层的湿法处理步骤"},
            {"id": "submethod_016", "name": "快速退火（RTA）", "description": "沉积后短时高温退火，用于改善薄膜结晶性与界面质量"},
            {"id": "submethod_017", "name": "原位反射高能电子衍射（RHEED）", "description": "用于原位监控薄膜生长速率与均匀性的表征手段"},
        ]

        # 材料节点数据
        self.Material = [
            {"id": "material_001", "name": "Al", "description": "金属材料，导电性好，成本低，但熔点低，抗电迁移能力差，曾用于主流互连"},
            {"id": "material_002", "name": "Cu", "description": "金属材料，导电性和抗电迁移性极佳，但易扩散到硅中，必须与阻挡层搭配使用，是现代互连主流材料"},
            {"id": "material_003", "name": "TiN/TaN", "description": "金属材料，超薄阻挡层，主要作为阻挡层，阻止Cu扩散；兼具良好导电性和粘附性；TiN的功函数使其也用于栅电极"},
            {"id": "material_004", "name": "W", "description": "金属材料，填充性极佳，用于通孔（Via）和局部互连；耐高温；但电阻率较高，应力大"},
            {"id": "material_005", "name": "SiO₂", "description": "简单氧化物，硅基薄膜，绝缘性和化学稳定性极好，是经典的栅氧和介质材料；但k值（~3.9）较高，不适用于先进节点互连"},
            {"id": "material_006", "name": "Si₃N₄", "description": "介质材料，硅基薄膜，刻蚀选择性高，常用作刻蚀停止层和侧墙；应力大；k值高（~7）；对杂质有良好阻挡性"},
            {"id": "material_007", "name": "HfO₂", "description": "高k介质，氧化物半导体薄膜，高k值（~25）允许在等效氧化层厚度（EOT）更小时物理厚度更大，减少栅泄漏；需良好的热稳定性和可靠性"},
            {"id": "material_008", "name": "Poly-Si", "description": "半导体材料，硅基薄膜，耐高温，可与传统栅氧工艺兼容；功函数可通过掺杂调节；但存在耗尽效应，现已被金属栅替代"},
            {"id": "material_009", "name": "a-C", "description": "硬掩模材料，刻蚀选择性极高，用作硬掩模；硬度高；在多重图形化技术中保证图形转移保真度"},
            {"id": "material_010", "name": "GaN/GaAs", "description": "单晶半导体，化合物半导体薄膜，宽带隙适用于高功率、高频；高电子迁移率；高击穿电场；GaN基材料发光效率高，用于LED"},
            {"id": "material_011", "name": "ITO", "description": "简单氧化物，氧化物半导体薄膜"},
            {"id": "material_012", "name": "Ti", "description": "金属材料"},
            {"id": "material_013", "name": "TiW", "description": "合金材料"},
            {"id": "material_014", "name": "USG", "description": "介质材料，硅基薄膜"},
            {"id": "material_015", "name": "PSG", "description": "介质材料，硅基薄膜"},
            {"id": "material_016", "name": "BPSG", "description": "介质材料，硅基薄膜"},
            {"id": "material_017", "name": "a-Si", "description": "半导体材料，硅基薄膜"},
            {"id": "material_018", "name": "Al₂O₃", "description": "高k介质，氧化物半导体薄膜"},
            {"id": "material_019", "name": "ZrO₂", "description": "高k介质，氧化物半导体薄膜"},
            {"id": "material_020", "name": "InP", "description": "化合物半导体，化合物半导体薄膜"},
            {"id": "material_021", "name": "AlGaInP", "description": "化合物半导体，化合物半导体薄膜"},
            {"id": "material_022", "name": "Si", "description": "单晶半导体，硅基薄膜"},
            {"id": "material_023", "name": "SiGe", "description": "单晶半导体，硅基薄膜"},
            {"id": "material_024", "name": "Ge", "description": "24.Ge：单晶半导体，化合物半导体薄膜"},
            {"id": "material_025", "name": "InGaZnO", "description": "半导体通道，氧化物半导体薄膜"},
            {"id": "material_026", "name": "CoSi₂", "description": "由于其具有低电阻率、良好的热稳定性以及与硅的良好晶格匹配等特性，广泛应用于大规模集成电路中，作为连接金属与半导体的材料"},
            {"id": "material_027", "name": "Ru", "description": "金属材料，具有极低的电阻率和良好的阻挡性能，有望替代铜作为未来互连材料"},
            {"id": "material_028", "name": "Mo", "description": "金属材料，高熔点，良好的热稳定性和导电性，用于特殊应用"},
            {"id": "material_029", "name": "Ta", "description": "金属材料，常用作铜互连的阻挡层材料"},
            {"id": "material_030", "name": "Ni", "description": "金属材料，用于接触层和硅化物形成"},
            {"id": "material_031", "name": "Pt", "description": "贵金属材料，高功函数，用于电极和存储器件"},
            {"id": "material_032", "name": "Au", "description": "贵金属材料，优异的导电性和稳定性，用于特殊应用"},
            {"id": "material_033", "name": "ZnO", "description": "氧化物半导体，透明导电材料，用于显示和光伏应用"},
            {"id": "material_034", "name": "SnO₂", "description": "氧化物半导体，透明导电材料，气敏特性"},
            {"id": "material_035", "name": "TiO₂", "description": "氧化物材料，高介电常数，用于电容和光催化"},
            {"id": "material_036", "name": "SiC", "description": "宽带隙半导体，高耐压、高频特性，用于功率器件"},
            {"id": "material_037", "name": "Diamond", "description": "超宽禁带半导体，极高的热导率和击穿场强"},
            {"id": "material_038", "name": "低k介质", "description": "低介电常数材料，如SiCOH，用于减少互连电容"},
            {"id": "material_039", "name": "高k金属栅", "description": "高k介质与金属栅的组合结构，用于先进CMOS技术"},
            {"id": "material_040", "name": "铁电材料", "description": "如HfZrO₂, PZT，具有铁电特性，用于存储器"},
            {"id": "material_041", "name": "相变材料", "description": "如GST(Ge₂Sb₂Te₅)，用于相变存储器"},
            {"id": "material_042", "name": "磁性材料", "description": "如CoFeB，用于磁性随机存取存储器(MRAM)"},
            {"id": "material_043", "name": "有机半导体", "description": "如并五苯，用于柔性电子和有机发光二极管"},
            {"id": "material_044", "name": "钙钛矿材料", "description": "如MAPbI₃，用于高效太阳能电池和发光器件"},
            {"id": "material_045", "name": "2D材料", "description": "如石墨烯、MoS₂，单原子层厚度，独特电学特性"},
            {"id": "material_046", "name": "多孔材料", "description": "如多孔SiO₂，极低介电常数，用于超低k介质"},
            {"id": "material_047", "name": "MXene", "description": "二维过渡金属碳化物/氮化物，高导电性，用于储能和电子器件"},
            {"id": "material_048", "name": "hBN", "description": "六方氮化硼，宽带隙绝缘体，优异的导热性和原子级平整表面"},
            {"id": "material_049", "name": "AlScN", "description": "氮化铝钪，具有铁电特性的新型压电材料"},
            {"id": "material_050", "name": "LiNbO₃", "description": "铌酸锂，优异的电光和压电特性，用于调制器和传感器"},
            {"id": "material_051", "name": "VO₂", "description": "二氧化钒，具有金属-绝缘体相变特性，用于智能窗和开关器件"},
            {"id": "material_052", "name": "SiCOH", "description": "含碳氧化硅，低k介质材料"},
            {"id": "material_053", "name": "Black Diamond", "description": "应用材料公司开发的低k介质材料"},
            {"id": "material_054", "name": "CoWP", "description": "钴钨磷，用于铜互连的帽层材料"},
            {"id": "material_055", "name": "RuTa", "description": "钌钽合金，新型互连材料"},
            {"id": "material_056", "name": "MoS₂", "description": "二硫化钼，二维半导体材料"},
            {"id": "material_057", "name": "WS₂", "description": "二硫化钨，二维半导体材料"},
            {"id": "material_058", "name": "Ga₂O₃", "description": "氧化镓，超宽禁带半导体"},
            {"id": "material_059", "name": "AlN", "description": "氮化铝，高热导率宽禁带半导体"},
            {"id": "material_060", "name": "ZnMgO", "description": "锌镁氧化物，可调带隙半导体"},
            {"id": "material_061", "name": "Y₂O₃", "description": "氧化钇，高k介质材料"},
            {"id": "material_062", "name": "La₂O₃", "description": "氧化镧，高k介质材料"},
            {"id": "material_063", "name": "SrTiO₃", "description": "钛酸锶，高k介质和铁电材料"},
            {"id": "material_064", "name": "Ge₂Sb₂Te₅", "description": "GST，相变存储材料"},
            {"id": "material_065", "name": "HfZrO₂", "description": "铪锆氧化物，铁电材料"},
            {"id": "material_066", "name": "Al-doped ZnO", "description": "AZO，透明导电氧化物"},
            {"id": "material_067", "name": "In-doped ZnO", "description": "IZO，透明导电氧化物"},
            {"id": "material_068", "name": "SrRuO₃", "description": "钌酸锶，导电氧化物电极"},
            {"id": "material_069", "name": "LaNiO₃", "description": "镍酸镧，导电氧化物电极"},
            {"id": "material_070", "name": "YBa₂Cu₃O₇", "description": "YBCO，高温超导材料"},
            # 新型半导体材料
            {"id": "material_071", "name": "Ga₂O₃", "description": "氧化镓，超宽禁带半导体材料"},
            {"id": "material_072", "name": "β-Ga₂O₃", "description": "β相氧化镓，具有优异功率特性"},
            {"id": "material_073", "name": "ZnO纳米线", "description": "氧化锌纳米线，用于传感器和光电器件"},
            {"id": "material_074", "name": "SiC纳米管", "description": "碳化硅纳米管，高强度和热稳定性"},

            # 新型二维材料
            {"id": "material_075", "name": "黑磷", "description": "磷烯，具有可调带隙的二维材料"},
            {"id": "material_076", "name": "ReS₂", "description": "二硫化铼，各向异性二维半导体"},
            {"id": "material_077", "name": "PtSe₂", "description": "二硒化铂，空气稳定的二维材料"},
            {"id": "material_078", "name": "Janus二维材料", "description": "两面化学组成不同的二维材料"},

            # 新型功能材料
            {"id": "material_079", "name": "多铁性材料", "description": "同时具有铁电和铁磁特性的材料"},
            {"id": "material_080", "name": "拓扑绝缘体", "description": "体内绝缘表面导电的特殊材料"},
            {"id": "material_081", "name": "Weyl半金属", "description": "具有Weyl费米子的拓扑材料"},
            {"id": "material_082", "name": "MOF材料", "description": "金属有机框架材料，高比表面积"},

            # 生物兼容材料
            {"id": "material_083", "name": "导电聚合物", "description": "PEDOT:PSS等生物兼容导电材料"},
            {"id": "material_084", "name": "水凝胶", "description": "具有生物相容性的智能材料"},
            {"id": "material_085", "name": "丝素蛋白", "description": "天然生物材料，良好的生物相容性"},
            {"id": "material_086", "name": "有机-无机杂化钙钛矿", "description": "结合有机和无机材料优势的钙钛矿材料"},
            {"id": "material_087", "name": "共价有机框架", "description": "COF，具有精确孔道结构的有机晶体材料"},
            {"id": "material_088", "name": "液态金属", "description": "室温下呈液态的金属材料，用于柔性电子"},
            {"id": "material_089", "name": "量子点发光材料", "description": "具有量子限域效应的纳米发光材料"},
            {"id": "material_090", "name": "多孔硅", "description": "具有纳米孔洞的硅材料，用于传感和生物应用"},

        
            {"id": "material_091", "name": "铝", "description": "用于金属互连层的材料。"},
            {"id": "material_092", "name": "铜", "description": "用于金属互连层的材料。"},
            {"id": "material_093", "name": "氮化钛", "description": "用于屏障层的材料。"},
            {"id": "material_094", "name": "二氧化硅", "description": "CVD工艺沉积的介质层材料。"},
            {"id": "material_095", "name": "氮化硅", "description": "CVD工艺沉积的介质层材料。"},
            {"id": "material_096", "name": "多晶硅", "description": "用于栅极的材料。"},]

        # 能力节点数据
        self.Capability = [
            {"id": "capability_001", "name": "高沉积速率", "description": "量单位时间内的产膜厚度，直接关乎生产效率。受前驱体利用率和反应活性影响"},
            {"id": "capability_002", "name": "大腔体/大面积均匀性", "description": "指在超大尺寸基片（如玻璃基板）上膜厚和成分的均匀性，对设备设计（气路、温场）要求极高"},
            {"id": "capability_003", "name": "低温工艺(<400°C)", "description": "工艺温度越低，对基底热预算影响越小，越适合后端工艺。常通过等离子体增强（如PECVD, PE-ALD）实现"},
            {"id": "capability_004", "name": "超薄薄膜 & 原子级厚度控制", "description": "指对薄膜厚度无与伦比的精度和可控性，其根本机制是自限制反应（ALD）"},
            {"id": "capability_005", "name": "高纯度 & 高质量薄膜", "description": "指薄膜中杂质少（纯度高）、针孔等缺陷密度低、结构致密、内应力可控"},
            {"id": "capability_006", "name": "无与伦比的保形性", "description": "物理过程，用于半导体材料的物理处理"},
            {"id": "capability_007", "name": "低成本", "description": "综合评估设备、运行、材料和维护成本。可扩展性（如卷对卷生产）和材料利用率是关键因素"},
            {"id": "capability_013", "name": "热管理", "description": "控制和管理芯片热量的能力"},
            {"id": "capability_014", "name": "应力控制", "description": "精确控制薄膜内应力的能力"},
            {"id": "capability_015", "name": "掺杂控制", "description": "精确控制材料掺杂浓度和分布的能力"},
            {"id": "capability_016", "name": "界面优化", "description": "优化不同材料间界面特性的能力"},
            {"id": "capability_017", "name": "缺陷工程", "description": "通过控制缺陷改善材料性能的能力"},
            {"id": "capability_018", "name": "晶向控制", "description": "控制晶体生长方向的能力"},
            {"id": "capability_008", "name": "选择性沉积", "description": "仅在特定表面或区域沉积材料的能力"},
            {"id": "capability_009", "name": "区域控制", "description": "对不同区域实现不同材料或厚度的精确控制"},
            {"id": "capability_010", "name": "成分梯度控制", "description": "实现薄膜成分在厚度或平面方向的梯度变化"},
            {"id": "capability_011", "name": "界面工程", "description": "精确控制界面结构和化学状态，优化器件性能"},
            {"id": "capability_012", "name": "三维结构保形性", "description": "在复杂三维结构表面实现均匀覆盖的能力"},
            {"id": "capability_019", "name": "纳米级图案化", "description": "实现纳米尺度图案制备的能力"},
            {"id": "capability_020", "name": "多层结构控制", "description": "精确控制多层薄膜结构的能力"},
            {"id": "capability_021", "name": "原位监测与控制", "description": "实时监测和控制沉积过程的能力"},
            {"id": "capability_022", "name": "环境稳定性", "description": "薄膜在特定环境下的稳定性"},
            {"id": "capability_023", "name": "可扩展性", "description": "技术向大面积扩展的能力"},
            {"id": "capability_024", "name": "量子相干控制", "description": "控制和维持量子相干性的能力"},
            {"id": "capability_025", "name": "自旋极化控制", "description": "控制电子自旋极化的能力"},
            {"id": "capability_026", "name": "拓扑态调控", "description": "调控材料拓扑电子态的能力"},
            {"id": "capability_027", "name": "生物兼容性", "description": "材料与生物体相容的能力"},
            {"id": "capability_028", "name": "可降解性", "description": "材料在特定条件下分解的能力"},
            {"id": "capability_029", "name": "自修复能力", "description": "材料自动修复损伤的能力"},
            {"id": "capability_030", "name": "形状记忆", "description": "材料记住并恢复原始形状的能力"},
            {"id": "capability_031", "name": "神经形态计算效率", "description": "模拟神经计算的能效比"},
            {"id": "capability_032", "name": "生物信号灵敏度", "description": "检测生物电信号的灵敏度"},
            {"id": "capability_033", "name": "环境适应性", "description": "在不同环境条件下的工作稳定性"},
            {"id": "capability_034", "name": "能量转换效率", "description": "将其他能量转换为电能的效率"},
            {"id": "capability_035", "name": "太赫兹响应特性", "description": "在太赫兹频段的电磁响应特性"},
        
            {"id": "capability_036", "name": "台阶覆盖性", "description": "PVD工艺（如磁控溅射）具有良好的台阶覆盖性。"},
            {"id": "capability_037", "name": "高纯度", "description": "PVD工艺（如磁控溅射）具有高纯度。"},
            {"id": "capability_038", "name": "高度共形", "description": "CVD工艺能实现高度共形、均匀的薄膜沉积。"},
            {"id": "capability_039", "name": "均匀", "description": "CVD工艺能实现高度共形、均匀的薄膜沉积。"},
            {"id": "capability_040", "name": "亚纳米级的厚度控制", "description": "原子层沉积能实现亚纳米级的厚度控制。"},
            {"id": "capability_041", "name": "极致共形性", "description": "原子层沉积能实现极致共形性。"},]

        # 设备节点数据
        self.Equipment = [
            {"id": "equipment_001", "name": "溅射台", "description": "用于溅射工艺的设备"},
            {"id": "equipment_002", "name": "蒸发台", "description": "用于蒸发工艺的设备"},
            {"id": "equipment_003", "name": "离子镀膜机", "description": "用于离子镀膜工艺的设备"},
            {"id": "equipment_004", "name": "PLD系统", "description": "用于脉冲激光沉积工艺的设备"},
            {"id": "equipment_005", "name": "APCVD反应器", "description": "用于常压化学气相沉积工艺的设备"},
            {"id": "equipment_006", "name": "LPCVD炉管", "description": "用于低压化学气相沉积工艺的设备"},
            {"id": "equipment_007", "name": "MOCVD反应器", "description": "用于金属有机化学气相沉积工艺的设备"},
            {"id": "equipment_008", "name": "ALD系统", "description": "用于原子层沉积工艺的设备"},
            {"id": "equipment_009", "name": "PE-ALD系统", "description": "用于等离子体增强原子层沉积工艺的设备"},
            {"id": "equipment_010", "name": "匀胶机/旋涂仪", "description": "用于旋涂工艺的设备"},
            {"id": "equipment_011", "name": "狭缝涂布机", "description": "用于狭缝涂布工艺的设备"},
            {"id": "equipment_012", "name": "喷墨打印机", "description": "用于喷墨打印工艺的设备"},
            {"id": "equipment_013", "name": "MBE系统", "description": "用于分子束外延工艺的设备"},
            {"id": "equipment_014", "name": "VPE系统", "description": "用于气相外延工艺的设备"},
            {"id": "equipment_015", "name": "LPE系统", "description": "用于液相外延工艺的设备"},
            {"id": "equipment_016", "name": "ECR-CVD系统", "description": "用于电子回旋共振化学气相沉积的设备"},
            {"id": "equipment_017", "name": "HWCVD系统", "description": "用于热丝化学气相沉积的设备"},
            {"id": "equipment_018", "name": "IBAD系统", "description": "用于离子束辅助沉积的设备"},
            {"id": "equipment_019", "name": "HIPIMS系统", "description": "用于高功率脉冲磁控溅射的设备"},
            {"id": "equipment_020", "name": "溶胶-凝胶涂布设备", "description": "用于溶胶-凝胶法制备薄膜的设备"},
            {"id": "equipment_021", "name": "电纺丝设备", "description": "用于电纺丝法制备纳米纤维膜的设备"},
            {"id": "equipment_022", "name": "分子自组装系统", "description": "用于分子自组装制备有序薄膜的设备"},
            {"id": "equipment_028", "name": "TSV刻蚀系统", "description": "用于硅通孔刻蚀的设备"},
            {"id": "equipment_029", "name": "电镀系统", "description": "用于铜互连电镀的设备"},
            {"id": "equipment_030", "name": "化学机械抛光系统", "description": "CMP，用于晶圆全局平坦化的设备"},
            {"id": "equipment_031", "name": "晶圆键合机", "description": "用于晶圆对准和键合的设备"},
            {"id": "equipment_032", "name": "激光退火系统", "description": "用于局部退火的设备"},
            {"id": "equipment_033", "name": "离子注入机", "description": "用于掺杂的离子注入设备"},
            {"id": "equipment_034", "name": "纳米压印系统", "description": "用于纳米压印光刻的设备"},
            {"id": "equipment_035", "name": "原子力显微镜", "description": "AFM，用于表面形貌和特性分析"},
            {"id": "equipment_036", "name": "扫描电子显微镜", "description": "SEM，用于高分辨率表面成像"},
            {"id": "equipment_023", "name": "喷雾热解系统", "description": "用于喷雾热解法制备薄膜的设备"},
            {"id": "equipment_024", "name": "原子层刻蚀系统", "description": "用于原子层刻蚀工艺的设备"},
            {"id": "equipment_025", "name": "选区沉积系统", "description": "用于选择性沉积工艺的设备"},
            {"id": "equipment_026", "name": "分子层沉积系统", "description": "用于分子层沉积工艺的设备"},
            {"id": "equipment_027", "name": "原位监测系统", "description": "集成在沉积设备中用于实时监测薄膜生长的系统"},
            {"id": "equipment_041", "name": "椭圆偏振仪", "description": "用于测量薄膜厚度和光学常数（折射率、消光系数）的设备"},
            {"id": "equipment_042", "name": "紫外可见分光光度计", "description": "用于测量材料在紫外-可见光区域的吸收和透射特性的设备"},
            {"id": "equipment_043", "name": "飞秒激光系统", "description": "用于超快激光加工和沉积"},
            {"id": "equipment_044", "name": "低温沉积系统", "description": "可在极低温度下进行沉积的设备"},
            {"id": "equipment_045", "name": "超高真空互联系统", "description": "多个工艺腔室互联的超高真空系统"},
            {"id": "equipment_046", "name": "量子比特测试系统", "description": "用于量子比特性能测试的设备"},
            {"id": "equipment_047", "name": "自旋测量系统", "description": "测量电子自旋相关特性的设备"},
            {"id": "equipment_048", "name": "生物兼容沉积系统", "description": "专为生物材料沉积设计的设备"},
            {"id": "equipment_049", "name": "神经形态测试系统", "description": "测试神经形态器件性能的专业设备"},
            {"id": "equipment_050", "name": "生物安全沉积系统", "description": "符合生物安全标准的薄膜沉积设备"},
            {"id": "equipment_051", "name": "太赫兹测试系统", "description": "测试太赫兹器件性能的设备"},
            {"id": "equipment_052", "name": "超表面制造系统", "description": "制造超表面结构的专用设备"},
            {"id": "equipment_053", "name": "可持续制造评估系统", "description": "评估制造过程环境影响的系统"},
        ]

        # 制造阶段节点数据
        self.ManufacturingStage = [
            {"id": "stage_001", "name": "前道工艺", "description": "涉及晶体管等有源器件的制造"},
            {"id": "stage_002", "name": "后道工艺", "description": "涉及金属互联、介质层的制造"},
            {"id": "stage_003", "name": "中道工艺", "description": "介于前道和后道之间的工艺，如接触形成"},
            {"id": "stage_004", "name": "先进封装", "description": "包括2.5D/3D封装等先进封装技术"},
        
            {"id": "stage_005", "name": "沉积", "description": "半导体沉积工艺是现代集成电路制造中的核心步骤之一。"},]

        # 芯片结构节点数据
        self.ChipStructure = [
            {"id": "structure_001", "name": "栅极", "description": "包含栅介质和金属栅"},
            {"id": "structure_002", "name": "高k栅介质", "description": "如HfO₂, ZrO₂等具有高介电常数的栅介质材料"},
            {"id": "structure_003", "name": "金属栅", "description": "如TiN, TaN等金属材料制成的栅电极"},
            {"id": "structure_004", "name": "侧墙", "description": "如Si₃N₄, SiO₂等材料制成的侧墙结构"},
            {"id": "structure_005", "name": "浅沟槽隔离", "description": "用于晶体管之间的电学隔离"},
            {"id": "structure_006", "name": "接触孔", "description": "连接栅/漏/源与第一层金属"},
            {"id": "structure_007", "name": "金属互连线", "description": "包括导线和通孔(Via)"},
            {"id": "structure_008", "name": "阻挡层/衬垫", "description": "如TaN/Ta, TiN, 用于防止金属扩散"},
            {"id": "structure_009", "name": "种子层", "description": "如Cu, 用于电镀"},
            {"id": "structure_010", "name": "介质层", "description": "ILD, IMD等层间介质，如SiO₂, 低k材料"},
            {"id": "structure_011", "name": "钝化层", "description": "最外层的保护层，如Si₃N₄, SiON"},
            {"id": "structure_012", "name": "硬掩膜", "description": "如Si₃N₄, α-Si, 用于图形化转移"},
            {"id": "structure_013", "name": "高深宽比间隙填充", "description": "用于填充高纵横比的间隙"},
            {"id": "structure_014", "name": "超薄阻挡层", "description": "极薄的阻挡层，通常由ALD技术制备"},
            {"id": "structure_015", "name": "存储节点", "description": "如电容、相变材料、铁电材料等用于数据存储的结构"},
            {"id": "structure_016", "name": "互连通孔", "description": "连接不同金属层的垂直通道"},
            {"id": "structure_017", "name": "空气隙", "description": "极低k介质结构，通过引入空气降低介电常数"},
            {"id": "structure_018", "name": "鳍式结构", "description": "FinFET中的鳍状有源区结构"},
            {"id": "structure_019", "name": "纳米线", "description": "一维纳米结构，用于未来晶体管设计"},
            {"id": "structure_020", "name": "二维通道", "description": "基于二维材料的晶体管通道"},
            {"id": "structure_021", "name": "量子点", "description": "纳米尺度量子限制结构，用于新型器件"},
            {"id": "structure_022", "name": "光子晶体", "description": "周期性介电结构，用于光子器件"},
            {"id": "structure_023", "name": "硅通孔", "description": "TSV，用于3D集成的垂直互连"},
            {"id": "structure_024", "name": "微凸块", "description": "Microbump，用于芯片堆叠的微小连接点"},
            {"id": "structure_025", "name": "再分布层", "description": "RDL，重新分布芯片焊盘位置的金属层"},
            {"id": "structure_026", "name": "中介层", "description": "Interposer，连接不同芯片的中间载体"},
            {"id": "structure_027", "name": "量子比特", "description": "量子计算的基本单元"},
            {"id": "structure_028", "name": "自旋阀", "description": "基于电子自旋的磁存储结构"},
            {"id": "structure_029", "name": "忆阻器", "description": "具有记忆特性的电阻器，用于神经形态计算"},
            {"id": "structure_030", "name": "光子集成电路", "description": "PIC，集成光学元件的芯片"},
            # 新兴应用领域
            {"id": "structure_031", "name": "神经形态器件", "description": "模拟生物神经网络的电子器件"},
            {"id": "structure_032", "name": "柔性电子", "description": "可弯曲、可拉伸的电子器件"},
            {"id": "structure_033", "name": "透明电子", "description": "透明或半透明的电子器件"},
            {"id": "structure_034", "name": "可穿戴器件", "description": "可穿戴设备中的电子元件"},
            {"id": "structure_035", "name": "自旋轨道耦合器", "description": "利用自旋轨道耦合效应的器件"},
            {"id": "structure_036", "name": "拓扑量子比特", "description": "基于拓扑材料的量子比特"},
            {"id": "structure_037", "name": "神经形态突触", "description": "模拟生物突触的电子器件"},
            {"id": "structure_038", "name": "生物传感器", "description": "用于生物分子检测的传感器"},
            {"id": "structure_039", "name": "柔性电极", "description": "可弯曲拉伸的电极结构"},
            {"id": "structure_040", "name": "微流控通道", "description": "用于流体控制的微米尺度通道"},
            {"id": "structure_041", "name": "神经形态计算阵列", "description": "模拟生物神经网络的大规模计算阵列"},
            {"id": "structure_042", "name": "生物-电子接口", "description": "连接生物组织与电子器件的界面结构"},
            {"id": "structure_043", "name": "能量收集器", "description": "从环境中收集能量的微纳结构"},
            {"id": "structure_044", "name": "太赫兹器件", "description": "工作在太赫兹频段的电子器件"},
            {"id": "structure_045", "name": "超表面", "description": "具有亚波长结构的人工电磁表面"},

        
            {"id": "structure_046", "name": "金属互连层", "description": "PVD工艺广泛用于制备金属互连层。"},
            {"id": "structure_047", "name": "屏障层", "description": "PVD工艺广泛用于制备屏障层。"},
            {"id": "structure_048", "name": "高深宽比结构", "description": "原子层沉积适用于高深宽比结构中的沉积。"},]

        # 参数节点数据
        self.Parameter = [
            {"id": "parameter_001", "name": "厚度", "description": "薄膜的物理厚度。常用度量标准/单位：纳米 (nm), 埃 (Å)"},
            {"id": "parameter_002", "name": "均匀性", "description": "薄膜厚度或性质在晶圆内（WIW）或晶圆间（WTW）的一致性。常用度量标准/单位：1σ (%) 或 Range (%)"},
            {"id": "parameter_003", "name": "粗糙度", "description": "薄膜表面的不平整程度。影响后续层沉积和电学性能。常用度量标准/单位：RMS (均方根粗糙度) (nm)"},
            {"id": "parameter_004", "name": "应力", "description": "薄膜内存在的内应力，可能导致晶圆翘曲或薄膜剥落。常用度量标准/单位：MPa (兆帕) (张应力为+, 压应力为-)"},
            {"id": "parameter_005", "name": "电阻率", "description": "衡量薄膜导电能力的参数。常用度量标准/单位：μΩ·cm (微欧·厘米) (金属)，Ω·cm (欧·厘米) (半导体)"},
            {"id": "parameter_006", "name": "漏电流", "description": "通过绝缘介质薄膜的微小电流。直接影响器件功耗和可靠性。常用度量标准/单位：A/cm² (每平方厘米安培) @ 特定电场强度 (MV/cm)"},
            {"id": "parameter_007", "name": "台阶覆盖率", "description": "薄膜覆盖台阶结构的能力，是保形性的量化体现。常用度量标准/单位：SC% = (侧壁厚度 / 顶部厚度) × 100%"},
            {"id": "parameter_008", "name": "缺陷密度", "description": "单位面积内的针孔、颗粒等缺陷的数量。常用度量标准/单位：个/cm² (每平方厘米个数)"},
            {"id": "parameter_009", "name": "纯度", "description": "薄膜中目标材料的含量，杂质元素越少越好。常用度量标准/单位：% (百分比) 或 原子浓度 (atoms/cm³)"},
            {"id": "parameter_010", "name": "介电常数", "description": "材料存储电荷能力的量度。常用度量标准/单位：k值 (无单位)"},
            {"id": "parameter_011", "name": "能带隙", "description": "价带顶到导带底的能量差。常用度量标准/单位：eV (电子伏特)"},
            {"id": "parameter_012", "name": "载流子迁移率", "description": "载流子在电场作用下的移动速度。常用度量标准/单位：cm²/V·s"},
            {"id": "parameter_013", "name": "击穿场强", "description": "材料发生电击穿的临界电场强度。常用度量标准/单位：MV/cm"},
            {"id": "parameter_014", "name": "热导率", "description": "材料传导热量的能力。常用度量标准/单位：W/m·K"},
            {"id": "parameter_015", "name": "光学带隙", "description": "材料吸收光子的最小能量。常用度量标准/单位：eV (电子伏特)"},
            {"id": "parameter_016", "name": "折射率", "description": "光在真空中的速度与在材料中速度的比值。常用度量标准/单位：n (无单位)"},
            {"id": "parameter_017", "name": "消光系数", "description": "材料吸收光能力的量度。常用度量标准/单位：k (无单位)"},
            {"id": "parameter_018", "name": "杨氏模量", "description": "材料刚度的量度。常用度量标准/单位：GPa"},
            {"id": "parameter_019", "name": "硬度", "description": "材料抵抗局部变形的能力。常用度量标准/单位：GPa"},
            {"id": "parameter_025", "name": "热膨胀系数", "description": "材料在温度变化时的膨胀率。常用度量标准/单位：ppm/K"},
            {"id": "parameter_026", "name": "热阻", "description": "材料阻碍热量传递的能力。常用度量标准/单位：K/W"},
            {"id": "parameter_027", "name": "载流子寿命", "description": "载流子在复合前存在的时间。常用度量标准/单位：μs"},
            {"id": "parameter_028", "name": "陷阱密度", "description": "材料中电荷陷阱的密度。常用度量标准/单位：个/cm³"},
            {"id": "parameter_029", "name": "相干时间", "description": "量子比特保持量子相干性的时间。常用度量标准/单位：μs"},
            {"id": "parameter_030", "name": "自旋弛豫时间", "description": "电子自旋状态弛豫的时间。常用度量标准/单位：ns"},
            {"id": "parameter_020", "name": "选择性", "description": "沉积或刻蚀过程中对不同材料的选择比。常用度量标准/单位：选择比 (无单位)"},
            {"id": "parameter_021", "name": "界面态密度", "description": "半导体-介质界面处的缺陷态密度。常用度量标准/单位：个/eV·cm²"},
            {"id": "parameter_022", "name": "铁电矫顽场", "description": "使铁电材料极化反转所需的电场强度。常用度量标准/单位：kV/cm"},
            {"id": "parameter_023", "name": "压电系数", "description": "材料压电效应的强度。常用度量标准/单位：pm/V"},
            {"id": "parameter_024", "name": "相变温度", "description": "材料发生相变的温度。常用度量标准/单位：°C 或 K"},
            {"id": "parameter_034", "name": "量子相干时间", "description": "量子态保持相干的时间。常用度量标准/单位：μs, ms"},
            {"id": "parameter_035", "name": "自旋弛豫时间", "description": "自旋极化衰减的时间。常用度量标准/单位：ns"},
            {"id": "parameter_036", "name": "拓扑不变量", "description": "表征拓扑相的数理量。常用度量标准/单位：无单位"},
            {"id": "parameter_037", "name": "生物兼容性指数", "description": "材料生物兼容性的量化指标。常用度量标准/单位：无单位"},
            {"id": "parameter_038", "name": "降解速率", "description": "材料降解的速度。常用度量标准/单位：mg/day"},
            {"id": "parameter_039", "name": "自修复效率", "description": "材料自修复能力的量化。常用度量标准/单位：%"},
            {"id": "parameter_040", "name": "铁磁矫顽力", "description": "使铁磁材料磁化反转所需的磁场强度。常用度量标准/单位：Oe"},
            {"id": "parameter_041", "name": "磁致伸缩系数", "description": "材料在磁场中长度变化的比率。常用度量标准 /单位：ppm"},
            {"id": "parameter_042", "name": "铁磁居里温度", "description": "铁磁材料转变为顺磁性的温度。常用度量标准/单位：°C 或 K"},
            {"id": "parameter_043", "name": "神经突触权重", "description": "神经形态器件中突触连接的权重值"},
            {"id": "parameter_044", "name": "生物兼容性等级", "description": "材料与生物组织相容性的分级指标"},
            {"id": "parameter_045", "name": "能量收集密度", "description": "单位面积收集的能量功率"},
            {"id": "parameter_046", "name": "太赫兹吸收率", "description": "材料对太赫兹波的吸收能力"},
            {"id": "parameter_047", "name": "相位调控精度", "description": "超表面对电磁波相位调控的精度"},
        ]
        self.relationships = [
            # 技术大类与技术大类
            {"start_id": "tech_003", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "ALD技术属于CVD技术"},

            # 技术大类与反应类型的关系
            {"start_id": "tech_001", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "PVD技术属于物理过程"},
            {"start_id": "tech_002", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "CVD技术属于化学过程"},
            {"start_id": "tech_003", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "ALD技术属于化学过程"},
            {"start_id": "tech_004", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "溶液法属于物理过程"},
            {"start_id": "tech_005", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "外延生长属于物理过程"},
            {"start_id": "tech_005", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "外延生长属于化学过程"},
            {"start_id": "tech_009", "end_id": "action_003", "relationship_type": "HAS_ACTION", "weight": 1, "description": "电化学沉积技术属于电化学过程"},
            {"start_id": "tech_010", "end_id": "action_005", "relationship_type": "HAS_ACTION", "weight": 1, "description": "等离子体技术属于等离子体过程"},
            {"start_id": "tech_011", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "激光加工技术属于物理过程"},

            # 方法与技术大类的关系
            {"start_id": "method_001", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "溅射属于PVD技术"},
            {"start_id": "method_002", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "蒸镀属于PVD技术"},
            {"start_id": "method_003", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "离子镀属于PVD技术"},
            {"start_id": "method_004", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "PLD属于PVD技术"},
            {"start_id": "method_005", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "PECVD属于CVD技术"},
            {"start_id": "method_006", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "MOCVD属于CVD技术"},
            {"start_id": "method_007", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "APCVD属于CVD技术"},
            {"start_id": "method_008", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "LPCVD属于CVD技术"},
            {"start_id": "method_022", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "SACVD属于CVD技术"},
            {"start_id": "method_036", "end_id": "tech_006", "relationship_type": "BELONGS_TO", "weight": 1, "description": "TSV填充属于3D集成技术"},
            {"start_id": "method_037", "end_id": "tech_006", "relationship_type": "BELONGS_TO", "weight": 1, "description": "晶圆键合属于3D集成技术"},
            {"start_id": "method_038", "end_id": "tech_007", "relationship_type": "BELONGS_TO", "weight": 1, "description": "选择性外延属于异质集成技术"},
            {"start_id": "method_039", "end_id": "tech_008", "relationship_type": "BELONGS_TO", "weight": 1, "description": "纳米压印用于量子器件制造"},

            {"start_id": "method_009", "end_id": "tech_003", "relationship_type": "BELONGS_TO", "weight": 1, "description": "热ALD属于ALD技术"},
            {"start_id": "method_010", "end_id": "tech_003", "relationship_type": "BELONGS_TO", "weight": 1, "description": "PE-ALD属于ALD技术"},
            {"start_id": "method_011", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "旋涂属于溶液法"},
            {"start_id": "method_012", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "喷墨打印属于溶液法"},
            {"start_id": "method_013", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "狭缝涂布属于溶液法"},
            {"start_id": "method_014", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "Langmuir-Blodgett属于溶液法"},
            {"start_id": "method_015", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "电化学沉积属于溶液法"},
            {"start_id": "method_016", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "水热/溶剂热法属于溶液法"},
            {"start_id": "method_017", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "凹版印刷属于溶液法"},
            {"start_id": "method_018", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "丝网印刷属于溶液法"},
            {"start_id": "method_019", "end_id": "tech_005", "relationship_type": "BELONGS_TO", "weight": 1, "description": "MBE属于外延生长技术"},
            {"start_id": "method_020", "end_id": "tech_005", "relationship_type": "BELONGS_TO", "weight": 1, "description": "LPE属于外延生长技术"},
            {"start_id": "method_021", "end_id": "tech_005", "relationship_type": "BELONGS_TO", "weight": 1, "description": "VPE属于外延生长技术"},

            {"start_id": "method_023", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "ECR-CVD属于CVD技术"},
            {"start_id": "method_024", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "HWCVD属于CVD技术"},
            {"start_id": "method_025", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "Cat-CVD属于CVD技术"},
            {"start_id": "method_026", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "IBAD属于PVD技术"},
            {"start_id": "method_027", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "ECR-PVD属于PVD技术"},
            {"start_id": "method_028", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "溶胶-凝胶法属于溶液法"},
            {"start_id": "method_029", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "电纺丝属于溶液法"},
            {"start_id": "method_030", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "分子自组装属于溶液法"},

            {"start_id": "method_031", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "喷雾热解属于溶液法"},
            {"start_id": "method_032", "end_id": "tech_003", "relationship_type": "RELATED_TO", "weight": 1, "description": "原子层刻蚀与ALD技术相关"},
            {"start_id": "method_033", "end_id": "tech_003", "relationship_type": "RELATED_TO", "weight": 1, "description": "选择性地沉积与ALD技术相关"},
            {"start_id": "method_034", "end_id": "tech_003", "relationship_type": "BELONGS_TO", "weight": 1, "description": "区域选择性ALD属于ALD技术"},
            {"start_id": "method_035", "end_id": "tech_003", "relationship_type": "RELATED_TO", "weight": 1, "description": "分子层沉积与ALD技术相关"},
            {"start_id": "method_045", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "激光化学气相沉积属于CVD技术"},
            {"start_id": "method_046", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "电子束诱导沉积属于PVD技术"},
            {"start_id": "method_047", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "离子束沉积属于PVD技术"},
            {"start_id": "method_048", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "团簇束沉积属于PVD技术"},

            # 子方法与方法的关系
            {"start_id": "submethod_001", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "直流溅射属于溅射方法"},
            {"start_id": "submethod_002", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "射频溅射属于溅射方法"},
            {"start_id": "submethod_003", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "磁控溅射属于溅射方法"},
            {"start_id": "submethod_004", "end_id": "method_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "电子束蒸发属于蒸镀方法"},
            {"start_id": "submethod_005", "end_id": "method_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "热蒸发属于蒸镀方法"},
            {"start_id": "submethod_006", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "反应溅射属于溅射方法"},
            {"start_id": "submethod_007", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "共溅射属于溅射方法"},
            {"start_id": "submethod_008", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "HIPIMS属于溅射方法"},
            {"start_id": "submethod_009", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "激光辅助CVD属于CVD技术"},
            {"start_id": "submethod_010", "end_id": "tech_003", "relationship_type": "RELATED_TO", "weight": 1, "description": "原子层刻蚀与ALD技术相关"},

            # 方法节点与材料的关系
            # PVD
            {"start_id": "tech_001", "end_id": "material_001", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀Al"},
            {"start_id": "tech_001", "end_id": "material_002", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀Cu"},
            {"start_id": "tech_001", "end_id": "material_003", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀TiN"},
            {"start_id": "tech_001", "end_id": "material_013", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀TiW"},
            {"start_id": "tech_001", "end_id": "material_011", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀ITO"},
            {"start_id": "tech_001", "end_id": "material_005", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀SiO₂"},
            {"start_id": "tech_001", "end_id": "material_026", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀CoSi₂"},
            {"start_id": "tech_001", "end_id": "material_004", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀W"},
            {"start_id": "tech_001", "end_id": "material_027", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀Ru"},
            {"start_id": "tech_001", "end_id": "material_028", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀Mo"},
            {"start_id": "tech_001", "end_id": "material_029", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀Ta"},
            {"start_id": "tech_001", "end_id": "material_030", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀Ni"},
            {"start_id": "tech_001", "end_id": "material_031", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀Pt"},
            {"start_id": "tech_001", "end_id": "material_032", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀Au"},

            # CVD
            {"start_id": "tech_002", "end_id": "material_005", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀SiO₂"},
            {"start_id": "tech_002", "end_id": "material_006", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀Si₃N₄"},
            {"start_id": "tech_002", "end_id": "material_014", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀USG"},
            {"start_id": "tech_002", "end_id": "material_015", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀PSG"},
            {"start_id": "tech_002", "end_id": "material_016", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀BPSG"},
            {"start_id": "tech_002", "end_id": "material_008", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀Poly-Si"},
            {"start_id": "tech_002", "end_id": "material_017", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀a-Si"},
            {"start_id": "tech_002", "end_id": "material_009", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀a-C"},
            {"start_id": "tech_002", "end_id": "material_012", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀Ti"},
            {"start_id": "tech_002", "end_id": "material_033", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀ZnO"},
            {"start_id": "tech_002", "end_id": "material_034", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀SnO₂"},
            {"start_id": "tech_002", "end_id": "material_035", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀TiO₂"},
            {"start_id": "tech_002", "end_id": "material_036", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀SiC"},
            {"start_id": "tech_002", "end_id": "material_037", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀Diamond"},
            {"start_id": "tech_002", "end_id": "material_038", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀低k介质"},

            # ALD
            {"start_id": "tech_003", "end_id": "material_007", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀HfO₂"},
            {"start_id": "tech_003", "end_id": "material_018", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀Al₂O₃"},
            {"start_id": "tech_003", "end_id": "material_019", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀ZrO₂"},
            {"start_id": "tech_003", "end_id": "material_003", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀TiN/TaN"},
            {"start_id": "tech_003", "end_id": "material_025", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀InGaZnO"},
            {"start_id": "tech_003", "end_id": "material_039", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀高k金属栅"},
            {"start_id": "tech_003", "end_id": "material_040", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀铁电材料"},
            {"start_id": "tech_003", "end_id": "material_041", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀相变材料"},
            {"start_id": "tech_003", "end_id": "material_042", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀磁性材料"},
            {"start_id": "tech_003", "end_id": "material_064", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀GST相变材料"},
            {"start_id": "tech_003", "end_id": "material_065", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀HfZrO₂铁电材料"},
            {"start_id": "tech_002", "end_id": "material_066", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀AZO透明导电膜"},
            {"start_id": "tech_002", "end_id": "material_067", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀IZO透明导电膜"},
            {"start_id": "tech_005", "end_id": "material_068", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀SrRuO₃电极"},
            {"start_id": "tech_005", "end_id": "material_069", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀LaNiO₃电极"},
            {"start_id": "tech_005", "end_id": "material_070", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀YBCO超导材料"},

            # 溶液法
            {"start_id": "tech_004", "end_id": "material_043", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀有机半导体"},
            {"start_id": "tech_004", "end_id": "material_044", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀钙钛矿材料"},
            {"start_id": "tech_004", "end_id": "material_045", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀2D材料"},
            {"start_id": "tech_004", "end_id": "material_046", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀多孔材料"},

            # MOCVD
            {"start_id": "method_006", "end_id": "material_010", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "MOCVD擅长沉淀GaN/GaAs"},
            {"start_id": "method_006", "end_id": "material_020", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "MOCVD擅长沉淀InP"},
            {"start_id": "method_006", "end_id": "material_021", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "MOCVD擅长沉淀AlGaInP"},

            # 外延生长
            {"start_id": "tech_005", "end_id": "material_022", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀Si"},
            {"start_id": "tech_005", "end_id": "material_023", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀SiGe"},
            {"start_id": "tech_005", "end_id": "material_024", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀Ge"},
            {"start_id": "tech_005", "end_id": "material_010", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀GaN/GaAs"},

            {"start_id": "tech_002", "end_id": "material_052", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀SiCOH"},
            {"start_id": "tech_002", "end_id": "material_053", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀Black Diamond"},
            {"start_id": "tech_004", "end_id": "material_054", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "电化学沉积擅长沉淀CoWP"},
            {"start_id": "tech_001", "end_id": "material_055", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀RuTa"},
            {"start_id": "tech_003", "end_id": "material_056", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀MoS₂"},
            {"start_id": "tech_003", "end_id": "material_057", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀WS₂"},
            {"start_id": "tech_005", "end_id": "material_058", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀Ga₂O₃"},
            {"start_id": "tech_005", "end_id": "material_059", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀AlN"},
            {"start_id": "tech_005", "end_id": "material_060", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀ZnMgO"},
            {"start_id": "tech_003", "end_id": "material_061", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀Y₂O₃"},
            {"start_id": "tech_003", "end_id": "material_062", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀La₂O₃"},
            {"start_id": "tech_003", "end_id": "material_063", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀SrTiO₃"},
            {"start_id": "tech_003", "end_id": "material_047", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀MXene"},
            {"start_id": "tech_003", "end_id": "material_048", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀hBN"},
            {"start_id": "tech_002", "end_id": "material_049", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀AlScN"},
            {"start_id": "tech_005", "end_id": "material_050", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀LiNbO₃"},
            {"start_id": "method_031", "end_id": "material_051", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "喷雾热解擅长沉淀VO₂"},

            # 方法与能力的关系
            {"start_id": "tech_001", "end_id": "capability_001", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "PVD具有高沉积率的特点"},
            {"start_id": "method_007", "end_id": "capability_001", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "APCVD具有高沉积速率的特点"},
            {"start_id": "method_015", "end_id": "capability_001", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "ECD具有高沉积速率的特点"},
            {"start_id": "method_005", "end_id": "capability_002", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "PECVD具有大腔体/大面积均匀性的特点"},
            {"start_id": "method_007", "end_id": "capability_002", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "APCVD具有大腔体/大面积均匀性的特点"},
            {"start_id": "method_005", "end_id": "capability_003", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "PECVD具有低温工艺(<400°C)的特点"},
            {"start_id": "method_010", "end_id": "capability_003", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "PE-ALD具有低温工艺(<400°C)的特点"},
            {"start_id": "tech_004", "end_id": "capability_003", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有低温工艺(<400°C)的特点"},
            {"start_id": "tech_003", "end_id": "capability_004", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "ALD具有超薄薄膜 & 原子级厚度控制的特点"},
            {"start_id": "method_019", "end_id": "capability_005", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "MBE具有高纯度 & 高质量薄膜的特点"},
            {"start_id": "method_008", "end_id": "capability_005", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "LPCVD具有高纯度 & 高质量薄膜的特点"},
            {"start_id": "tech_003", "end_id": "capability_006", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "ALD具有无与伦比的保形性的特点"},
            {"start_id": "tech_004", "end_id": "capability_007", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法（旋涂、印刷）具有低成本的特点"},
            {"start_id": "method_026", "end_id": "capability_005", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "IBAD具有高纯度高质量薄膜的特点"},
            {"start_id": "method_027", "end_id": "capability_006", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "ECR-PVD具有优异保形性的特点"},
            {"start_id": "method_028", "end_id": "capability_007", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶胶-凝胶法具有低成本的特点"},
            {"start_id": "method_029", "end_id": "capability_010", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "电纺丝具有成分梯度控制的特点"},
            {"start_id": "method_030", "end_id": "capability_011", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "分子自组装具有界面工程的特点"},
            {"start_id": "submethod_008", "end_id": "capability_005", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "HIPIMS具有高纯度高质量薄膜的特点"},
            {"start_id": "submethod_010", "end_id": "capability_004", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "原子层刻蚀具有原子级精度控制的特点"},
            {"start_id": "method_036", "end_id": "capability_006", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "TSV填充需要优异的保形性"},
            {"start_id": "method_037", "end_id": "capability_014", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "晶圆键合需要精确的应力控制"},
            {"start_id": "method_038", "end_id": "capability_008", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "选择性外延具有选择性沉积的特点"},
            {"start_id": "method_039", "end_id": "capability_007", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "纳米压印具有低成本的特点"},
            {"start_id": "method_040", "end_id": "capability_007", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "定向自组装具有低成本的特点"},
            {"start_id": "method_041", "end_id": "capability_004", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "原子级抛光具有原子级精度控制"},
            {"start_id": "method_042", "end_id": "capability_017", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "激光退火用于缺陷工程"},
            {"start_id": "method_043", "end_id": "capability_015", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "离子注入用于掺杂控制"},
            {"start_id": "method_044", "end_id": "capability_016", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "等离子体处理用于界面优化"},
            {"start_id": "method_032", "end_id": "capability_004", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "原子层刻蚀具有原子级精度控制的特点"},
            {"start_id": "method_033", "end_id": "capability_008", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "选择性地沉积具有选择性沉积的特点"},
            {"start_id": "method_034", "end_id": "capability_009", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "区域选择性ALD具有区域控制的特点"},
            {"start_id": "method_035", "end_id": "capability_011", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "分子层沉积具有界面工程的特点"},
            {"start_id": "tech_003", "end_id": "capability_012", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "ALD具有优异的三维结构保形性"},
            {"start_id": "method_039", "end_id": "capability_019", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "纳米压印具有纳米级图案化能力"},
            {"start_id": "method_040", "end_id": "capability_019", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "定向自组装具有纳米级图案化能力"},
            {"start_id": "tech_003", "end_id": "capability_020", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "ALD具有优异的多层结构控制能力"},
            {"start_id": "method_019", "end_id": "capability_020", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "MBE具有优异的多层结构控制能力"},
            {"start_id": "equipment_027", "end_id": "capability_021", "relationship_type": "ENABLES", "weight": 1, "description": "原位监测系统实现原位监测与控制"},

            # 方法与设备的关系
            {"start_id": "method_001", "end_id": "equipment_001", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "溅射需要溅射台"},
            {"start_id": "method_002", "end_id": "equipment_002", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "蒸发需要蒸发台"},
            {"start_id": "method_003", "end_id": "equipment_003", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "离子镀需要离子镀膜机"},
            {"start_id": "method_004", "end_id": "equipment_004", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "PLD需要PLD系统"},
            {"start_id": "method_007", "end_id": "equipment_005", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "APCVD需要APCVD反应器"},
            {"start_id": "method_008", "end_id": "equipment_006", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "LPCVD需要LPCVD炉管"},
            {"start_id": "method_006", "end_id": "equipment_007", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "MOCVD需要MOCVD反应器"},
            {"start_id": "method_009", "end_id": "equipment_008", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "热ALD需要ALD系统"},
            {"start_id": "method_010", "end_id": "equipment_009", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "PE-ALD需要PE-ALD系统"},
            {"start_id": "method_011", "end_id": "equipment_010", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "旋涂需要匀胶机/旋涂仪"},
            {"start_id": "method_013", "end_id": "equipment_011", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "狭缝涂布需要狭缝涂布机"},
            {"start_id": "method_012", "end_id": "equipment_012", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "喷墨打印需要喷墨打印机"},
            {"start_id": "method_019", "end_id": "equipment_013", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "MBE需要MBE系统"},
            {"start_id": "method_021", "end_id": "equipment_014", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "VPE需要VPE系统"},
            {"start_id": "method_020", "end_id": "equipment_015", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "LPE需要LPE系统"},
            {"start_id": "method_023", "end_id": "equipment_016", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "ECR-CVD需要ECR-CVD系统"},
            {"start_id": "method_024", "end_id": "equipment_017", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "HWCVD需要HWCVD系统"},
            {"start_id": "method_026", "end_id": "equipment_018", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "IBAD需要IBAD系统"},
            {"start_id": "submethod_008", "end_id": "equipment_019", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "HIPIMS需要HIPIMS系统"},
            {"start_id": "method_028", "end_id": "equipment_020", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "溶胶-凝胶法需要溶胶-凝胶涂布设备"},
            {"start_id": "method_029", "end_id": "equipment_021", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "电纺丝需要电纺丝设备"},
            {"start_id": "method_030", "end_id": "equipment_022", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "分子自组装需要分子自组装系统"},
            {"start_id": "method_036", "end_id": "equipment_028", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "TSV填充需要TSV刻蚀系统"},
            {"start_id": "method_015", "end_id": "equipment_029", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "电化学沉积需要电镀系统"},
            {"start_id": "method_041", "end_id": "equipment_030", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "原子级抛光需要CMP系统"},
            {"start_id": "method_037", "end_id": "equipment_031", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "晶圆键合需要晶圆键合机"},
            {"start_id": "method_042", "end_id": "equipment_032", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "激光退火需要激光退火系统"},
            {"start_id": "method_043", "end_id": "equipment_033", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "离子注入需要离子注入机"},
            {"start_id": "method_039", "end_id": "equipment_034", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "纳米压印需要纳米压印系统"},
            {"start_id": "method_031", "end_id": "equipment_023", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "喷雾热解需要喷雾热解系统"},
            {"start_id": "method_032", "end_id": "equipment_024", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "原子层刻蚀需要原子层刻蚀系统"},
            {"start_id": "method_033", "end_id": "equipment_025", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "选择性地沉积需要选区沉积系统"},
            {"start_id": "method_035", "end_id": "equipment_026", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "分子层沉积需要分子层沉积系统"},
            {"start_id": "tech_003", "end_id": "equipment_027", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "ALD常配备原位监测系统"},
            {"start_id": "method_045", "end_id": "equipment_037", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "激光化学气相沉积需要LCVD系统"},
            {"start_id": "method_046", "end_id": "equipment_038", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "电子束诱导沉积需要EBID系统"},
            {"start_id": "method_047", "end_id": "equipment_039", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "离子束沉积需要IBD系统"},
            {"start_id": "method_048", "end_id": "equipment_040", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "团簇束沉积需要CBD系统"},
            # 技术与芯片结构的关系
            {"start_id": "tech_003", "end_id": "structure_002", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD主要用于高k栅介质"},
            {"start_id": "tech_003", "end_id": "structure_003", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD主要用于金属栅"},
            {"start_id": "method_008", "end_id": "structure_004", "relationship_type": "USED_FOR", "weight": 1, "description": "LPCVD主要用于侧墙"},
            {"start_id": "method_001", "end_id": "structure_008", "relationship_type": "USED_FOR", "weight": 1, "description": "PVD主要用于阻挡层/衬垫"},
            {"start_id": "method_001", "end_id": "structure_009", "relationship_type": "USED_FOR", "weight": 1, "description": "PVD主要用于种子层"},
            {"start_id": "tech_003", "end_id": "structure_014", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD主要用于超薄阻挡层"},
            {"start_id": "method_005", "end_id": "structure_010", "relationship_type": "USED_FOR", "weight": 1, "description": "PECVD主要用于介质层"},
            {"start_id": "method_005", "end_id": "structure_011", "relationship_type": "USED_FOR", "weight": 1, "description": "PECVD主要用于钝化层"},
            {"start_id": "method_005", "end_id": "structure_012", "relationship_type": "USED_FOR", "weight": 1, "description": "PECVD主要用于硬掩膜"},
            {"start_id": "method_022", "end_id": "structure_013", "relationship_type": "USED_FOR", "weight": 1, "description": "SACVD用于高深宽比间隙填充"},
            {"start_id": "method_008", "end_id": "structure_006", "relationship_type": "USED_FOR", "weight": 1, "description": "LPCVD主要用于深沟槽隔离"},
            {"start_id": "tech_003", "end_id": "structure_015", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于存储节点"},
            {"start_id": "tech_003", "end_id": "structure_016", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于互连通孔"},
            {"start_id": "tech_003", "end_id": "structure_017", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于空气隙结构"},
            {"start_id": "tech_003", "end_id": "structure_018", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于鳍式结构"},
            {"start_id": "tech_003", "end_id": "structure_019", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于纳米线"},
            {"start_id": "tech_003", "end_id": "structure_020", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于二维通道"},
            {"start_id": "tech_003", "end_id": "structure_021", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于量子点"},
            {"start_id": "tech_003", "end_id": "structure_022", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于光子晶体"},

            # 芯片结构与技术的关系
            {"start_id": "structure_023", "end_id": "tech_006", "relationship_type": "MANUFACTURED_BY", "weight": 1, "description": "硅通孔由3D集成技术制造"},
            {"start_id": "structure_024", "end_id": "tech_006", "relationship_type": "MANUFACTURED_BY", "weight": 1, "description": "微凸块由3D集成技术制造"},
            {"start_id": "structure_025", "end_id": "tech_006", "relationship_type": "MANUFACTURED_BY", "weight": 1, "description": "再分布层由3D集成技术制造"},
            {"start_id": "structure_026", "end_id": "tech_006", "relationship_type": "MANUFACTURED_BY", "weight": 1, "description": "中介层由3D集成技术制造"},
            {"start_id": "structure_027", "end_id": "tech_008", "relationship_type": "MANUFACTURED_BY", "weight": 1, "description": "量子比特由量子器件制造技术制造"},
            {"start_id": "structure_028", "end_id": "tech_007", "relationship_type": "MANUFACTURED_BY", "weight": 1, "description": "自旋阀由异质集成技术制造"},
            {"start_id": "structure_029", "end_id": "tech_007", "relationship_type": "MANUFACTURED_BY", "weight": 1, "description": "忆阻器由异质集成技术制造"},
            {"start_id": "structure_030", "end_id": "tech_007", "relationship_type": "MANUFACTURED_BY", "weight": 1, "description": "光子集成电路由异质集成技术制造"},

            # 芯片结构之间的关系
            {"start_id": "structure_002", "end_id": "structure_001", "relationship_type": "PART_OF", "weight": 1, "description": "高k栅介质是栅极的一部分"},
            {"start_id": "structure_003", "end_id": "structure_001", "relationship_type": "PART_OF", "weight": 1, "description": "金属栅是栅极的一部分"},
            {"start_id": "structure_008", "end_id": "structure_007", "relationship_type": "PART_OF", "weight": 1, "description": "阻挡层是金属互连线的一部分"},
            {"start_id": "structure_013", "end_id": "structure_005", "relationship_type": "APPLIED_TO", "weight": 1, "description": "高深宽比间隙填充应用于浅沟槽隔离"},
            {"start_id": "structure_015", "end_id": "structure_001", "relationship_type": "PART_OF", "weight": 1, "description": "存储节点是存储器的一部分"},
            {"start_id": "structure_016", "end_id": "structure_007", "relationship_type": "PART_OF", "weight": 1, "description": "互连通孔是金属互连线的一部分"},
            {"start_id": "structure_017", "end_id": "structure_010", "relationship_type": "PART_OF", "weight": 1, "description": "空气隙是介质层的一部分"},
            {"start_id": "structure_018", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "鳍式结构制造于前道工艺"},
            {"start_id": "structure_019", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "纳米线制造于前道工艺"},
            {"start_id": "structure_020", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "二维通道制造于前道工艺"},

            # 芯片结构与制造阶段的关系
            {"start_id": "structure_001", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "栅极制造于前道工艺"},
            {"start_id": "structure_004", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "侧墙制造于前道工艺"},
            {"start_id": "structure_005", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "浅沟槽隔离制造于前道工艺"},
            {"start_id": "structure_007", "end_id": "stage_002", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "金属互连线制造于后道工艺"},
            {"start_id": "structure_010", "end_id": "stage_002", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "介质层制造于后道工艺"},
            # 参数相关关系
            # PVD相关参数
            {"start_id": "tech_001", "end_id": "parameter_005", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "PVD制备的薄膜具有低电阻率(接近体材料值，如Cu~1.7μΩcm)"},
            {"start_id": "tech_001", "end_id": "capability_001", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "PVD通常具有高沉积速率(可达每分钟数百至数千埃)"},
            {"start_id": "tech_001", "end_id": "parameter_007", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "PVD其缺点是低台阶覆盖率(通常为10%-50%)"},
            {"start_id": "tech_001", "end_id": "parameter_004", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "PVD可能引入中等应力(通常为压应力)"},
            {"start_id": "tech_001", "end_id": "parameter_003", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "PVD表面具有中等粗糙度(RMS~1-5nm)"},

            # LPCVD/APCVD相关参数
            {"start_id": "method_008", "end_id": "parameter_008", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "LPCVD制备的薄膜具有高质量、低缺陷密度(致密)"},
            {"start_id": "method_007", "end_id": "parameter_008", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "APCVD制备的薄膜具有高质量、低缺陷密度(致密)"},
            {"start_id": "method_008", "end_id": "parameter_007", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "LPCVD擅长良好的台阶覆盖率(80%-95%)"},
            {"start_id": "method_007", "end_id": "parameter_007", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "APCVD擅长良好的台阶覆盖率(80%-95%)"},
            {"start_id": "method_008", "end_id": "capability_001", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "LPCVD通常具有中等沉积速率(每分钟数十至数百埃)"},
            {"start_id": "method_007", "end_id": "capability_001", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "APCVD通常具有中等沉积速率(每分钟数十至数百埃)"},
            {"start_id": "method_008", "end_id": "parameter_004", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "LPCVD可能产生高应力(LPCVDSi₃N₄为高张应力)"},
            {"start_id": "method_008", "end_id": "parameter_003", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "LPCVD表面具有低粗糙度(RMS<1nm)"},

            # PECVD相关参数
            {"start_id": "method_005", "end_id": "parameter_006", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "PECVD由于等离子体损伤，可能具有高漏电流(与热CVD相比)"},
            {"start_id": "method_005", "end_id": "parameter_007", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "PECVD制备的薄膜具有中等台阶覆盖率(50%-80%)"},
            {"start_id": "method_005", "end_id": "parameter_004", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "PECVD通常具有中等应力(可通过配方调节)"},

            # ALD相关参数
            {"start_id": "tech_003", "end_id": "parameter_007", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ALD在台阶覆盖率上表现极佳(~100%，甚至对超高深宽比结构)"},
            {"start_id": "tech_003", "end_id": "parameter_001", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ALD在厚度控制上表现极佳(原子级精度，±0.1Å/cycle)"},
            {"start_id": "tech_003", "end_id": "parameter_002", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ALD制备的薄膜具有极致均匀性(WIW<1%)"},
            {"start_id": "tech_003", "end_id": "parameter_003", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ALD制备的薄膜具有极低粗糙度(RMS<0.5nm)"},
            {"start_id": "tech_003", "end_id": "capability_001", "relationship_type": "HAS_DISADVANTAGE", "weight": 1, "description": "ALD其缺点是极低沉积速率(每小时数十至数百埃)"},

            # MOCVD相关参数
            {"start_id": "method_006", "end_id": "parameter_002", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "MOCVD在大面积均匀性上表现极佳(适用于大外延片)"},
            {"start_id": "method_006", "end_id": "parameter_009", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "MOCVD制备的薄膜具有高纯度、单晶质量(用于化合物半导体)"},

            # 电化学沉积相关参数
            {"start_id": "method_015", "end_id": "parameter_007", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "电化学沉积(ECD)在填充性上表现极佳(超级填充，无空洞)"},
            {"start_id": "method_015", "end_id": "parameter_005", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "电化学沉积(ECD)制备的薄膜具有低电阻率(块体铜值)"},
            {"start_id": "method_015", "end_id": "capability_001", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "电化学沉积(ECD)其优点是极高沉积速率(每分钟数千埃)"},

            {"start_id": "material_007", "end_id": "parameter_010", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "HfO₂具有高介电常数(k~25)"},
            {"start_id": "material_038", "end_id": "parameter_010", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "低k介质具有低介电常数(k<3.0)"},
            {"start_id": "material_036", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "SiC具有宽带隙(3.2-3.3eV)"},
            {"start_id": "material_037", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "金刚石具有超宽带隙(5.5eV)"},
            {"start_id": "material_045", "end_id": "parameter_012", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "2D材料具有高载流子迁移率"},
            {"start_id": "material_036", "end_id": "parameter_013", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "SiC具有高击穿场强(2-4MV/cm)"},
            {"start_id": "material_037", "end_id": "parameter_014", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "金刚石具有极高热导率(2000W/m·K)"},
            {"start_id": "material_011", "end_id": "parameter_015", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ITO具有宽光学带隙(>3.5eV)"},
            {"start_id": "material_011", "end_id": "parameter_016", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ITO具有特定折射率(~2.0)"},
            {"start_id": "material_037", "end_id": "parameter_018", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "金刚石具有高杨氏模量(1050GPa)"},
            {"start_id": "material_037", "end_id": "parameter_019", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "金刚石具有极高硬度(100GPa)"},
            {"start_id": "material_059", "end_id": "parameter_014", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "AlN具有高热导率"},
            {"start_id": "material_058", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Ga₂O₃具有超宽禁带(~4.8eV)"},
            {"start_id": "material_056", "end_id": "parameter_012", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "MoS₂具有适中的载流子迁移率"},
            {"start_id": "material_063", "end_id": "parameter_010", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "SrTiO₃具有高介电常数(~300)"},
            {"start_id": "material_054", "end_id": "parameter_005", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "CoWP具有低电阻率"},
            {"start_id": "material_055", "end_id": "parameter_005", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "RuTa具有低电阻率"},
            {"start_id": "material_047", "end_id": "parameter_005", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "MXene具有高电导率"},
            {"start_id": "material_048", "end_id": "parameter_014", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "hBN具有高导热性"},
            {"start_id": "material_049", "end_id": "parameter_022", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "AlScN具有铁电特性"},
            {"start_id": "material_049", "end_id": "parameter_023", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "AlScN具有高压电系数"},
            {"start_id": "material_050", "end_id": "parameter_023", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "LiNbO₃具有高压电系数"},
            {"start_id": "material_051", "end_id": "parameter_024", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "VO₂具有相变特性"},
            {"start_id": "material_064", "end_id": "parameter_024", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "GST具有相变特性"},
            {"start_id": "material_065", "end_id": "parameter_022", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "HfZrO₂具有铁电特性"},
            {"start_id": "material_066", "end_id": "parameter_005", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "AZO具有低电阻率"},
            {"start_id": "material_070", "end_id": "parameter_031", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "YBCO具有超导转变温度"},
            # 检测设备与参数的关系
            {"start_id": "equipment_035", "end_id": "parameter_003", "relationship_type": "MEASURES", "weight": 1, "description": "原子力显微镜测量表面粗糙度"},
            {"start_id": "equipment_035", "end_id": "parameter_001", "relationship_type": "MEASURES", "weight": 1, "description": "原子力显微镜测量薄膜厚度"},
            {"start_id": "equipment_036", "end_id": "parameter_007", "relationship_type": "MEASURES", "weight": 1, "description": "扫描电子显微镜测量台阶覆盖率"},
            {"start_id": "equipment_036", "end_id": "parameter_008", "relationship_type": "MEASURES", "weight": 1, "description": "扫描电子显微镜检测缺陷密度"},

            # 芯片结构与材料的关系
            {"start_id": "structure_023", "end_id": "material_002", "relationship_type": "MADE_FROM", "weight": 1, "description": "硅通孔常用铜填充"},
            {"start_id": "structure_024", "end_id": "material_030", "relationship_type": "MADE_FROM", "weight": 1, "description": "微凸块常用锡银合金或铜"},
            {"start_id": "structure_025", "end_id": "material_002", "relationship_type": "MADE_FROM", "weight": 1, "description": "再分布层常用铜制成"},
            {"start_id": "structure_026", "end_id": "material_022", "relationship_type": "MADE_FROM", "weight": 1, "description": "中介层常用硅制成"},
            {"start_id": "structure_027", "end_id": "material_010", "relationship_type": "MADE_FROM", "weight": 1, "description": "量子比特常用超导材料如铌制成"},
            {"start_id": "structure_028", "end_id": "material_042", "relationship_type": "MADE_FROM", "weight": 1, "description": "自旋阀常用磁性材料制成"},
            {"start_id": "structure_029", "end_id": "material_041", "relationship_type": "MADE_FROM", "weight": 1, "description": "忆阻器常用过渡金属氧化物制成"},
            {"start_id": "structure_030", "end_id": "material_050", "relationship_type": "MADE_FROM", "weight": 1, "description": "光子集成电路常用铌酸锂等材料制成"},
            # 芯片结构与应用的关系
            {"start_id": "structure_018", "end_id": "material_023", "relationship_type": "MADE_FROM", "weight": 1, "description": "鳍式结构常由SiGe制成"},
            {"start_id": "structure_019", "end_id": "material_022", "relationship_type": "MADE_FROM", "weight": 1, "description": "纳米线常由Si制成"},
            {"start_id": "structure_020", "end_id": "material_045", "relationship_type": "MADE_FROM", "weight": 1, "description": "二维通道由2D材料制成"},
            {"start_id": "structure_021", "end_id": "material_010", "relationship_type": "MADE_FROM", "weight": 1, "description": "量子点常由GaAs/InP等化合物半导体制成"},

            # 新技术与制造阶段的关系
            {"start_id": "method_032", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "原子层刻蚀用于前道工艺"},
            {"start_id": "method_033", "end_id": "stage_002", "relationship_type": "USED_IN", "weight": 1, "description": "选择性地沉积用于后道工艺"},
            {"start_id": "method_034", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "区域选择性ALD用于前道工艺"},

            # 新参数定义
            {"id": "parameter_031", "name": "超导转变温度", "description": "材料从正常态转变为超导态的温度。常用度量标准/单位：K"},
            {"id": "parameter_032", "name": "载流子浓度", "description": "单位体积内的自由载流子数量。常用度量标准/单位：cm⁻³"},
            {"id": "parameter_033", "name": "薄膜密度", "description": "薄膜的致密程度。常用度量标准/单位：g/cm³"},

            # 新技术应用
            {"start_id": "method_045", "end_id": "structure_009", "relationship_type": "USED_FOR", "weight": 1, "description": "激光化学气相沉积用于选择性沉积种子层"},
            {"start_id": "method_046", "end_id": "structure_021", "relationship_type": "USED_FOR", "weight": 1, "description": "电子束诱导沉积用于量子点制备"},
            {"start_id": "method_047", "end_id": "structure_008", "relationship_type": "USED_FOR", "weight": 1, "description": "离子束沉积用于超薄阻挡层"},


            {"start_id": "tech_004", "end_id": "structure_032", "relationship_type": "USED_FOR", "weight": 1, "description": "溶液法用于柔性电子制造"},
            {"start_id": "tech_004", "end_id": "structure_033", "relationship_type": "USED_FOR", "weight": 1, "description": "溶液法用于透明电子制造"},
            {"start_id": "tech_004", "end_id": "structure_034", "relationship_type": "USED_FOR", "weight": 1, "description": "溶液法用于可穿戴器件制造"},
            {"start_id": "tech_003", "end_id": "structure_031", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于神经形态器件制造"},

            # 工艺组合优化
            {"start_id": "method_001", "end_id": "method_026", "relationship_type": "COMBINES_WITH", "weight": 0.8, "description": "溅射可与离子束辅助沉积结合改善薄膜质量"},
            {"start_id": "method_002", "end_id": "method_026", "relationship_type": "COMBINES_WITH", "weight": 0.8, "description": "蒸镀可与离子束辅助沉积结合改善薄膜质量"},
            {"start_id": "method_009", "end_id": "method_010", "relationship_type": "ALTERNATIVE_TO", "weight": 0.7, "description": "热ALD与PE-ALD互为低温工艺替代方案"},

            # 工艺改进关系
            {"start_id": "submethod_003", "end_id": "submethod_001", "relationship_type": "IMPROVES", "weight": 0.9, "description": "磁控溅射改进直流溅射的沉积速率和均匀性"},
            {"start_id": "submethod_008", "end_id": "submethod_003", "relationship_type": "IMPROVES", "weight": 0.8, "description": "HIPIMS改进磁控溅射的薄膜致密性"},

            {"start_id": "material_012", "end_id": "tech_001", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀Ti"},
            {"start_id": "material_013", "end_id": "tech_001", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "PVD擅长沉淀TiW"},
            {"start_id": "material_014", "end_id": "tech_002", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀USG"},
            {"start_id": "material_015", "end_id": "tech_002", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀PSG"},
            {"start_id": "material_016", "end_id": "tech_002", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀BPSG"},
            {"start_id": "material_017", "end_id": "tech_002", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀a-Si"},

            # 连接未被充分使用的方法节点
            {"start_id": "method_031", "end_id": "tech_004", "relationship_type": "BELONGS_TO", "weight": 1, "description": "喷雾热解属于溶液法"},
            {"start_id": "method_045", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "激光化学气相沉积属于CVD技术"},
            {"start_id": "method_046", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "电子束诱导沉积属于PVD技术"},
            {"start_id": "method_047", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "离子束沉积属于PVD技术"},
            {"start_id": "method_048", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "团簇束沉积属于PVD技术"},
            {"start_id": "method_049", "end_id": "tech_005", "relationship_type": "BELONGS_TO", "weight": 1, "description": "VPE-ALD属于外延生长技术"},
            {"start_id": "method_050", "end_id": "tech_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "PE-PLD属于PVD技术"},

            # 连接未被充分使用的子方法节点
            {"start_id": "submethod_009", "end_id": "tech_002", "relationship_type": "BELONGS_TO", "weight": 1, "description": "激光辅助CVD属于CVD技术"},
            {"start_id": "submethod_010", "end_id": "tech_003", "relationship_type": "RELATED_TO", "weight": 1, "description": "原子层刻蚀与ALD技术相关"},

            # 连接未被充分使用的能力节点
            {"start_id": "tech_001", "end_id": "capability_014", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "PVD具有应力控制能力"},
            {"start_id": "tech_002", "end_id": "capability_015", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "CVD具有掺杂控制能力"},
            {"start_id": "tech_003", "end_id": "capability_016", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "ALD具有界面优化能力"},
            {"start_id": "tech_005", "end_id": "capability_018", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "外延生长具有晶向控制能力"},
            {"start_id": "tech_004", "end_id": "capability_022", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有环境稳定性"},
            {"start_id": "tech_004", "end_id": "capability_023", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有可扩展性"},

            # 连接未被充分使用的设备节点
            {"start_id": "equipment_035", "end_id": "tech_001", "relationship_type": "USED_FOR_ANALYSIS", "weight": 1, "description": "AFM用于PVD薄膜分析"},
            {"start_id": "equipment_036", "end_id": "tech_002", "relationship_type": "USED_FOR_ANALYSIS", "weight": 1, "description": "SEM用于CVD薄膜分析"},
            {"start_id": "equipment_023", "end_id": "tech_004", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "喷雾热解需要喷雾热解系统"},
            {"start_id": "equipment_024", "end_id": "tech_003", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "原子层刻蚀需要原子层刻蚀系统"},
            {"start_id": "equipment_025", "end_id": "tech_003", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "选择性地沉积需要选区沉积系统"},
            {"start_id": "equipment_026", "end_id": "tech_003", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "分子层沉积需要分子层沉积系统"},

            # 连接未被充分使用的参数节点
            {"start_id": "material_002", "end_id": "parameter_032", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Cu具有载流子浓度参数"},
            {"start_id": "material_022", "end_id": "parameter_032", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Si具有载流子浓度参数"},
            {"start_id": "material_005", "end_id": "parameter_033", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "SiO₂具有薄膜密度参数"},
            {"start_id": "material_007", "end_id": "parameter_033", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "HfO₂具有薄膜密度参数"},
            {"start_id": "tech_001", "end_id": "parameter_033", "relationship_type": "AFFECTS_PARAMETER", "weight": 1, "description": "PVD工艺影响薄膜密度"},
            {"start_id": "tech_002", "end_id": "parameter_033", "relationship_type": "AFFECTS_PARAMETER", "weight": 1, "description": "CVD工艺影响薄膜密度"},

            # 连接未被充分使用的制造阶段节点
            {"start_id": "tech_006", "end_id": "stage_002", "relationship_type": "USED_IN", "weight": 1, "description": "3D集成技术主要用于后道工艺"},
            {"start_id": "tech_007", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "异质集成可用于前道工艺"},
            {"start_id": "tech_008", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "量子器件制造主要用于前道工艺"},
            {"start_id": "tech_009", "end_id": "stage_002", "relationship_type": "USED_IN", "weight": 1, "description": "电化学沉积技术主要用于后道工艺"},
            {"start_id": "tech_010", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "等离子体技术可用于前道工艺"},
            {"start_id": "tech_011", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "激光加工技术可用于前道工艺"},

            # 连接未被充分使用的芯片结构节点
            {"start_id": "structure_031", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "神经形态器件制造于前道工艺"},
            {"start_id": "structure_032", "end_id": "stage_002", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "柔性电子制造于后道工艺"},
            {"start_id": "structure_033", "end_id": "stage_002", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "透明电子制造于后道工艺"},
            {"start_id": "structure_034", "end_id": "stage_002", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "可穿戴器件制造于后道工艺"},

            # 连接反应类型与更多技术
            {"start_id": "tech_006", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "3D集成技术涉及物理过程"},
            {"start_id": "tech_007", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "异质集成涉及化学过程"},
            {"start_id": "tech_008", "end_id": "action_004", "relationship_type": "HAS_ACTION", "weight": 1, "description": "量子器件制造涉及热过程"},

            # 添加更多材料-参数关系
            {"start_id": "material_018", "end_id": "parameter_010", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Al₂O₃具有中等介电常数(k~9)"},
            {"start_id": "material_019", "end_id": "parameter_010", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ZrO₂具有高介电常数(k~25)"},
            {"start_id": "material_020", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "InP具有特定带隙(1.35eV)"},
            {"start_id": "material_021", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "AlGaInP具有可调带隙"},
            {"start_id": "material_022", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Si具有1.12eV带隙"},
            {"start_id": "material_023", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "SiGe具有可调带隙"},
            {"start_id": "material_024", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Ge具有0.67eV带隙"},

            # 添加更多技术-参数关系
            {"start_id": "tech_004", "end_id": "parameter_003", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "溶液法可能产生较高表面粗糙度"},
            {"start_id": "tech_005", "end_id": "parameter_009", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "外延生长可制备高纯度单晶薄膜"},
            {"start_id": "tech_006", "end_id": "parameter_025", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "3D集成技术需考虑热膨胀系数匹配"},
            {"start_id": "tech_007", "end_id": "parameter_021", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "异质集成需优化界面态密度"},

            # 确保所有参数都有相关关系
            {"start_id": "parameter_020", "end_id": "method_032", "relationship_type": "MEASURED_BY", "weight": 1, "description": "选择性由原子层刻蚀工艺实现"},
            {"start_id": "parameter_021", "end_id": "tech_003", "relationship_type": "OPTIMIZED_BY", "weight": 1, "description": "界面态密度可由ALD优化"},
            {"start_id": "parameter_022", "end_id": "material_040", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "铁电矫顽场表征铁电材料"},
            {"start_id": "parameter_023", "end_id": "material_049", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "压电系数表征压电材料"},
            {"start_id": "parameter_024", "end_id": "material_041", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "相变温度表征相变材料"},
            {"start_id": "parameter_025", "end_id": "material_022", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Si具有特定热膨胀系数"},
            {"start_id": "parameter_026", "end_id": "material_037", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "金刚石具有极低热阻"},
            {"start_id": "parameter_027", "end_id": "material_010", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "GaN具有较长载流子寿命"},
            {"start_id": "parameter_028", "end_id": "material_017", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "a-Si具有较高陷阱密度"},
            {"start_id": "parameter_029", "end_id": "structure_027", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "相干时间表征量子比特质量"},
            {"start_id": "parameter_030", "end_id": "structure_028", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "自旋弛豫时间表征自旋阀性能"},

            # 连接新兴应用领域
            {"start_id": "structure_031", "end_id": "material_041", "relationship_type": "MADE_FROM", "weight": 1, "description": "神经形态器件常用相变材料制成"},
            {"start_id": "structure_032", "end_id": "material_043", "relationship_type": "MADE_FROM", "weight": 1, "description": "柔性电子常用有机半导体制成"},
            {"start_id": "structure_033", "end_id": "material_011", "relationship_type": "MADE_FROM", "weight": 1, "description": "透明电子常用ITO等透明导体制成"},
            {"start_id": "structure_034", "end_id": "material_044", "relationship_type": "MADE_FROM", "weight": 1, "description": "可穿戴器件常用钙钛矿材料制成"},

            # 连接复合技术
            {"start_id": "method_049", "end_id": "tech_002", "relationship_type": "COMBINES", "weight": 1, "description": "VPE-ALD结合了VPE和ALD技术"},
            {"start_id": "method_050", "end_id": "tech_010", "relationship_type": "COMBINES", "weight": 1, "description": "PE-PLD结合了等离子体和PLD技术"},

            # 确保所有能力都有相关技术
            {"start_id": "capability_013", "end_id": "tech_006", "relationship_type": "IMPORTANT_FOR", "weight": 1, "description": "热管理对3D集成技术至关重要"},
            {"start_id": "capability_017", "end_id": "tech_005", "relationship_type": "IMPORTANT_FOR", "weight": 1, "description": "缺陷工程对外延生长很重要"},

            # 连接检测设备与更多参数
            {"start_id": "equipment_035", "end_id": "parameter_004", "relationship_type": "MEASURES", "weight": 1, "description": "AFM可测量薄膜应力"},
            {"start_id": "equipment_036", "end_id": "parameter_002", "relationship_type": "MEASURES", "weight": 1, "description": "SEM可评估薄膜均匀性"},

            # 消光系数与材料的关系
            {"start_id": "material_011", "end_id": "parameter_017", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ITO具有特定的消光系数"},
            {"start_id": "material_033", "end_id": "parameter_017", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ZnO具有特定的消光系数"},
            {"start_id": "material_034", "end_id": "parameter_017", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "SnO₂具有特定的消光系数"},
            {"start_id": "material_035", "end_id": "parameter_017", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "TiO₂具有特定的消光系数"},
            {"start_id": "material_066", "end_id": "parameter_017", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "AZO具有特定的消光系数"},
            {"start_id": "material_067", "end_id": "parameter_017", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "IZO具有特定的消光系数"},
            {"start_id": "material_025", "end_id": "parameter_017", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "InGaZnO具有特定的消光系数"},

            # 消光系数与光学应用的关系
            {"start_id": "parameter_017", "end_id": "structure_033", "relationship_type": "IMPORTANT_FOR", "weight": 1, "description": "消光系数对透明电子器件很重要"},
            {"start_id": "parameter_017", "end_id": "structure_030", "relationship_type": "IMPORTANT_FOR", "weight": 1, "description": "消光系数对光子集成电路很重要"},

            # 消光系数与检测设备的关系
            {"start_id": "equipment_041", "end_id": "parameter_017", "relationship_type": "MEASURES", "weight": 1, "description": "椭圆偏振仪测量消光系数"},
            {"start_id": "equipment_042", "end_id": "parameter_017", "relationship_type": "MEASURES", "weight": 1, "description": "紫外可见分光光度计测量消光系数"},

            # 消光系数与沉积技术的关系
            {"start_id": "tech_001", "end_id": "parameter_017", "relationship_type": "AFFECTS_PARAMETER", "weight": 1, "description": "PVD工艺影响薄膜消光系数"},
            {"start_id": "tech_002", "end_id": "parameter_017", "relationship_type": "AFFECTS_PARAMETER", "weight": 1, "description": "CVD工艺影响薄膜消光系数"},
            {"start_id": "tech_003", "end_id": "parameter_017", "relationship_type": "AFFECTS_PARAMETER", "weight": 1, "description": "ALD工艺影响薄膜消光系数"},

            # 消光系数与其他光学参数的关系
            {"start_id": "parameter_017", "end_id": "parameter_016", "relationship_type": "RELATED_TO", "weight": 1, "description": "消光系数与折射率共同决定材料光学性质"},
            {"start_id": "parameter_017", "end_id": "parameter_015", "relationship_type": "RELATED_TO", "weight": 1, "description": "消光系数与光学带隙相关"},

            {"start_id": "equipment_041", "end_id": "tech_001", "relationship_type": "USED_FOR_ANALYSIS", "weight": 1, "description": "椭圆偏振仪用于PVD薄膜光学分析"},
            {"start_id": "equipment_041", "end_id": "tech_002", "relationship_type": "USED_FOR_ANALYSIS", "weight": 1, "description": "椭圆偏振仪用于CVD薄膜光学分析"},
            {"start_id": "equipment_041", "end_id": "tech_003", "relationship_type": "USED_FOR_ANALYSIS", "weight": 1, "description": "椭圆偏振仪用于ALD薄膜光学分析"},
            {"start_id": "equipment_042", "end_id": "tech_004", "relationship_type": "USED_FOR_ANALYSIS", "weight": 1, "description": "紫外可见分光光度计用于溶液法薄膜光学分析"},

            # 连接新设备到相关材料
            {"start_id": "equipment_041", "end_id": "material_011", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "椭圆偏振仪表征ITO光学性质"},
            {"start_id": "equipment_042", "end_id": "material_033", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "紫外可见分光光度计表征ZnO光学性质"},

            # 连接新设备到相关应用
            {"start_id": "equipment_041", "end_id": "structure_033", "relationship_type": "USED_FOR", "weight": 1, "description": "椭圆偏振仪用于透明电子器件开发"},
            {"start_id": "equipment_042", "end_id": "structure_030", "relationship_type": "USED_FOR", "weight": 1, "description": "紫外可见分光光度计用于光子集成电路开发"},
            # 新技术与反应类型的关系
            {"start_id": "tech_012", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "纳米压印技术属于物理过程"},
            {"start_id": "tech_013", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "自组装技术属于化学过程"},
            {"start_id": "tech_014", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "混合沉积技术涉及物理过程"},
            {"start_id": "tech_014", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "混合沉积技术涉及化学过程"},

            # 新方法与技术的关系
            {"start_id": "method_051", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "热纳米压印属于纳米压印技术"},
            {"start_id": "method_052", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "紫外纳米压印属于纳米压印技术"},
            {"start_id": "method_054", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "嵌段共聚物自组装属于自组装技术"},
            {"start_id": "method_057", "end_id": "tech_014", "relationship_type": "BELONGS_TO", "weight": 1, "description": "PVD-CVD复合沉积属于混合沉积技术"},
            {"start_id": "method_060", "end_id": "tech_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "AI优化沉积属于智能沉积技术"},

            # 新材料与技术的关系
            {"start_id": "tech_005", "end_id": "material_071", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀Ga₂O₃"},
            {"start_id": "tech_003", "end_id": "material_075", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀黑磷"},
            {"start_id": "tech_004", "end_id": "material_083", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀导电聚合物"},

            # 新能力与技术的关系
            {"start_id": "tech_008", "end_id": "capability_024", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "量子器件制造具有量子相干控制能力"},
            {"start_id": "tech_007", "end_id": "capability_025", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "异质集成具有自旋极化控制能力"},
            {"start_id": "tech_004", "end_id": "capability_027", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有生物兼容性"},

            # 新设备与方法的关系
            {"start_id": "method_051", "end_id": "equipment_043", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "热纳米压印需要飞秒激光系统"},
            {"start_id": "method_060", "end_id": "equipment_045", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "AI优化沉积需要超高真空互联系统"},

            # 新结构与技术的关系
            {"start_id": "tech_008", "end_id": "structure_036", "relationship_type": "USED_FOR", "weight": 1, "description": "量子器件制造用于拓扑量子比特"},
            {"start_id": "tech_004", "end_id": "structure_038", "relationship_type": "USED_FOR", "weight": 1, "description": "溶液法用于生物传感器制造"},

            # 新参数与材料的关系
            {"start_id": "material_071", "end_id": "parameter_013", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Ga₂O₃具有高击穿场强(8MV/cm)"},
            {"start_id": "material_075", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "黑磷具有可调带隙(0.3-2.0eV)"},
            {"start_id": "material_083", "end_id": "parameter_037", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "导电聚合物具有生物兼容性"},

            # 新兴应用领域扩展
            {"start_id": "structure_037", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "神经形态突触制造于前道工艺"},
            {"start_id": "structure_038", "end_id": "stage_004", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "生物传感器制造于先进封装阶段"},

            # 工艺创新关系
            {"start_id": "method_057", "end_id": "tech_001", "relationship_type": "COMBINES", "weight": 0.9, "description": "PVD-CVD复合沉积结合PVD技术"},
            {"start_id": "method_057", "end_id": "tech_002", "relationship_type": "COMBINES", "weight": 0.9, "description": "PVD-CVD复合沉积结合CVD技术"},
            {"start_id": "method_058", "end_id": "tech_009", "relationship_type": "COMBINES", "weight": 0.9, "description": "电化学-ALD复合技术结合电化学沉积"},
            {"start_id": "method_058", "end_id": "tech_003", "relationship_type": "COMBINES", "weight": 0.9, "description": "电化学-ALD复合技术结合ALD技术"},

            # 智能优化关系
            {"start_id": "method_060", "end_id": "capability_001", "relationship_type": "OPTIMIZES", "weight": 0.8, "description": "AI优化沉积优化沉积速率"},
            {"start_id": "method_060", "end_id": "parameter_002", "relationship_type": "OPTIMIZES", "weight": 0.8, "description": "AI优化沉积优化均匀性参数"},
            {"start_id": "method_061", "end_id": "capability_021", "relationship_type": "ENHANCES", "weight": 0.9, "description": "实时过程控制增强原位监测能力"},

            # 材料特性关系
            {"start_id": "material_079", "end_id": "parameter_022", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "多铁性材料具有铁电特性"},
            {"start_id": "material_079", "end_id": "parameter_042", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "多铁性材料具有铁磁特性"},
            {"start_id": "material_080", "end_id": "parameter_036", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "拓扑绝缘体具有拓扑不变量"},

            # 检测与分析关系
            {"start_id": "equipment_046", "end_id": "parameter_034", "relationship_type": "MEASURES", "weight": 1, "description": "量子比特测试系统测量量子相干时间"},
            {"start_id": "equipment_047", "end_id": "parameter_035", "relationship_type": "MEASURES", "weight": 1, "description": "自旋测量系统测量自旋弛豫时间"},

            # 新兴技术交叉关系
            {"start_id": "tech_012", "end_id": "tech_008", "relationship_type": "COMPLEMENTS", "weight": 0.7, "description": "纳米压印技术补充量子器件制造"},
            {"start_id": "tech_013", "end_id": "tech_007", "relationship_type": "COMPLEMENTS", "weight": 0.7, "description": "自组装技术补充异质集成"},
            {"start_id": "tech_015", "end_id": "tech_014", "relationship_type": "ENHANCES", "weight": 0.8, "description": "智能沉积技术增强混合沉积技术"},
            {"start_id": "tech_012", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "纳米压印技术属于物理过程"},
            {"start_id": "tech_013", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "自组装技术属于化学过程"},
            {"start_id": "tech_014", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "混合沉积技术涉及物理过程"},
            {"start_id": "tech_014", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "混合沉积技术涉及化学过程"},
            {"start_id": "tech_015", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "智能沉积技术涉及物理过程"},
            {"start_id": "tech_015", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "智能沉积技术涉及化学过程"},

            # 连接未被充分使用的方法到技术
            {"start_id": "method_051", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "热纳米压印属于纳米压印技术"},
            {"start_id": "method_052", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "紫外纳米压印属于纳米压印技术"},
            {"start_id": "method_053", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "软纳米压印属于纳米压印技术"},
            {"start_id": "method_054", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "嵌段共聚物自组装属于自组装技术"},
            {"start_id": "method_055", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "DNA引导自组装属于自组装技术"},
            {"start_id": "method_056", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "胶体晶体自组装属于自组装技术"},
            {"start_id": "method_057", "end_id": "tech_014", "relationship_type": "BELONGS_TO", "weight": 1, "description": "PVD-CVD复合沉积属于混合沉积技术"},
            {"start_id": "method_058", "end_id": "tech_014", "relationship_type": "BELONGS_TO", "weight": 1, "description": "电化学-ALD复合技术属于混合沉积技术"},
            {"start_id": "method_059", "end_id": "tech_014", "relationship_type": "BELONGS_TO", "weight": 1, "description": "激光-溶液复合沉积属于混合沉积技术"},
            {"start_id": "method_060", "end_id": "tech_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "AI优化沉积属于智能沉积技术"},
            {"start_id": "method_061", "end_id": "tech_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "实时过程控制属于智能沉积技术"},
            {"start_id": "method_062", "end_id": "tech_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "数字孪生沉积属于智能沉积技术"},

            # 连接未被充分使用的材料到技术
            {"start_id": "tech_004", "end_id": "material_071", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀Ga₂O₃"},
            {"start_id": "tech_003", "end_id": "material_072", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀β-Ga₂O₃"},
            {"start_id": "tech_004", "end_id": "material_073", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀ZnO纳米线"},
            {"start_id": "tech_002", "end_id": "material_074", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀SiC纳米管"},
            {"start_id": "tech_003", "end_id": "material_075", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀黑磷"},
            {"start_id": "tech_003", "end_id": "material_076", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀ReS₂"},
            {"start_id": "tech_003", "end_id": "material_077", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀PtSe₂"},
            {"start_id": "tech_003", "end_id": "material_078", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀Janus二维材料"},
            {"start_id": "tech_005", "end_id": "material_079", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀多铁性材料"},
            {"start_id": "tech_005", "end_id": "material_080", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀拓扑绝缘体"},
            {"start_id": "tech_005", "end_id": "material_081", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀Weyl半金属"},
            {"start_id": "tech_004", "end_id": "material_082", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀MOF材料"},
            {"start_id": "tech_004", "end_id": "material_083", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀导电聚合物"},
            {"start_id": "tech_004", "end_id": "material_084", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀水凝胶"},
            {"start_id": "tech_004", "end_id": "material_085", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀丝素蛋白"},

            # 连接未被充分使用的能力到技术
            {"start_id": "tech_008", "end_id": "capability_024", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "量子器件制造具有量子相干控制能力"},
            {"start_id": "tech_007", "end_id": "capability_025", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "异质集成具有自旋极化控制能力"},
            {"start_id": "tech_007", "end_id": "capability_026", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "异质集成具有拓扑态调控能力"},
            {"start_id": "tech_004", "end_id": "capability_027", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有生物兼容性"},
            {"start_id": "tech_004", "end_id": "capability_028", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有可降解性"},
            {"start_id": "tech_004", "end_id": "capability_029", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有自修复能力"},
            {"start_id": "tech_004", "end_id": "capability_030", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有形状记忆能力"},

            # 连接未被充分使用的设备到方法
            {"start_id": "method_051", "end_id": "equipment_034", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "热纳米压印需要纳米压印系统"},
            {"start_id": "method_052", "end_id": "equipment_034", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "紫外纳米压印需要纳米压印系统"},
            {"start_id": "method_053", "end_id": "equipment_034", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "软纳米压印需要纳米压印系统"},
            {"start_id": "method_054", "end_id": "equipment_022", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "嵌段共聚物自组装需要分子自组装系统"},
            {"start_id": "method_055", "end_id": "equipment_022", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "DNA引导自组装需要分子自组装系统"},
            {"start_id": "method_056", "end_id": "equipment_022", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "胶体晶体自组装需要分子自组装系统"},
            {"start_id": "method_057", "end_id": "equipment_001", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "PVD-CVD复合沉积需要溅射台"},
            {"start_id": "method_057", "end_id": "equipment_005", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "PVD-CVD复合沉积需要APCVD反应器"},
            {"start_id": "method_060", "end_id": "equipment_045", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "AI优化沉积需要超高真空互联系统"},

            # 连接未被充分使用的芯片结构到技术
            {"start_id": "tech_008", "end_id": "structure_035", "relationship_type": "USED_FOR", "weight": 1, "description": "量子器件制造用于自旋轨道耦合器"},
            {"start_id": "tech_008", "end_id": "structure_036", "relationship_type": "USED_FOR", "weight": 1, "description": "量子器件制造用于拓扑量子比特"},
            {"start_id": "tech_003", "end_id": "structure_037", "relationship_type": "USED_FOR", "weight": 1, "description": "ALD用于神经形态突触"},
            {"start_id": "tech_004", "end_id": "structure_038", "relationship_type": "USED_FOR", "weight": 1, "description": "溶液法用于生物传感器"},
            {"start_id": "tech_004", "end_id": "structure_039", "relationship_type": "USED_FOR", "weight": 1, "description": "溶液法用于柔性电极"},
            {"start_id": "tech_004", "end_id": "structure_040", "relationship_type": "USED_FOR", "weight": 1, "description": "溶液法用于微流控通道"},

            # 连接未被充分使用的参数到材料
            {"start_id": "material_071", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Ga₂O₃具有超宽禁带(~4.8eV)"},
            {"start_id": "material_072", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "β-Ga₂O₃具有特定带隙(4.7-4.9eV)"},
            {"start_id": "material_073", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ZnO纳米线具有3.37eV带隙"},
            {"start_id": "material_074", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "SiC纳米管具有2.4-3.3eV带隙"},
            {"start_id": "material_075", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "黑磷具有可调带隙(0.3-2.0eV)"},
            {"start_id": "material_076", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ReS₂具有1.5eV带隙"},
            {"start_id": "material_077", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "PtSe₂具有1.2eV带隙"},
            {"start_id": "material_078", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Janus二维材料具有特定带隙"},
            {"start_id": "material_079", "end_id": "parameter_022", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "多铁性材料具有铁电特性"},
            {"start_id": "material_079", "end_id": "parameter_040", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "多铁性材料具有铁磁特性"},
            {"start_id": "material_080", "end_id": "parameter_036", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "拓扑绝缘体具有拓扑不变量"},
            {"start_id": "material_081", "end_id": "parameter_036", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Weyl半金属具有拓扑不变量"},
            {"start_id": "material_082", "end_id": "parameter_033", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "MOF材料具有高比表面积"},
            {"start_id": "material_083", "end_id": "parameter_005", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "导电聚合物具有适中电导率"},
            {"start_id": "material_083", "end_id": "parameter_037", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "导电聚合物具有生物兼容性"},
            {"start_id": "material_084", "end_id": "parameter_037", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "水凝胶具有生物兼容性"},
            {"start_id": "material_084", "end_id": "parameter_029", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "水凝胶具有自修复能力"},
            {"start_id": "material_085", "end_id": "parameter_037", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "丝素蛋白具有生物兼容性"},

            # 连接反应类型到更多技术
            {"start_id": "tech_009", "end_id": "action_003", "relationship_type": "HAS_ACTION", "weight": 1, "description": "电化学沉积技术属于电化学过程"},
            {"start_id": "tech_012", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "纳米压印技术属于物理过程"},
            {"start_id": "tech_013", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "自组装技术属于化学过程"},
            {"start_id": "tech_014", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "混合沉积技术涉及物理过程"},
            {"start_id": "tech_014", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "混合沉积技术涉及化学过程"},
            {"start_id": "tech_015", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "智能沉积技术涉及物理过程"},
            {"start_id": "tech_015", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "智能沉积技术涉及化学过程"},

            # 连接检测设备到更多参数
            {"start_id": "equipment_041", "end_id": "parameter_016", "relationship_type": "MEASURES", "weight": 1, "description": "椭圆偏振仪测量折射率"},
            {"start_id": "equipment_041", "end_id": "parameter_017", "relationship_type": "MEASURES", "weight": 1, "description": "椭圆偏振仪测量消光系数"},
            {"start_id": "equipment_041", "end_id": "parameter_001", "relationship_type": "MEASURES", "weight": 1, "description": "椭圆偏振仪测量薄膜厚度"},
            {"start_id": "equipment_042", "end_id": "parameter_015", "relationship_type": "MEASURES", "weight": 1, "description": "紫外可见分光光度计测量光学带隙"},
            {"start_id": "equipment_042", "end_id": "parameter_016", "relationship_type": "MEASURES", "weight": 1, "description": "紫外可见分光光度计测量折射率"},
            {"start_id": "equipment_042", "end_id": "parameter_017", "relationship_type": "MEASURES", "weight": 1, "description": "紫外可见分光光度计测量消光系数"},

            # 连接制造阶段到更多技术
            {"start_id": "tech_012", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "纳米压印技术用于前道工艺"},
            {"start_id": "tech_013", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "自组装技术用于前道工艺"},
            {"start_id": "tech_014", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "混合沉积技术用于前道工艺"},
            {"start_id": "tech_014", "end_id": "stage_002", "relationship_type": "USED_IN", "weight": 1, "description": "混合沉积技术用于后道工艺"},
            {"start_id": "tech_015", "end_id": "stage_001", "relationship_type": "USED_IN", "weight": 1, "description": "智能沉积技术用于前道工艺"},
            {"start_id": "tech_015", "end_id": "stage_002", "relationship_type": "USED_IN", "weight": 1, "description": "智能沉积技术用于后道工艺"},

            # 连接子方法到更多方法
            {"start_id": "submethod_011", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "等离子体增强溅射属于溅射方法"},
            {"start_id": "submethod_012", "end_id": "method_009", "relationship_type": "BELONGS_TO", "weight": 1, "description": "激光辅助ALD属于热ALD方法"},
            {"start_id": "submethod_013", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "磁场辅助沉积属于溅射方法"},
            {"start_id": "submethod_014", "end_id": "method_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "超声辅助沉积属于电化学沉积方法"},

            # 连接智能技术到能力
            {"start_id": "method_060", "end_id": "capability_001", "relationship_type": "OPTIMIZES", "weight": 1, "description": "AI优化沉积优化沉积速率"},
            {"start_id": "method_060", "end_id": "capability_002", "relationship_type": "OPTIMIZES", "weight": 1, "description": "AI优化沉积优化均匀性"},
            {"start_id": "method_060", "end_id": "capability_005", "relationship_type": "OPTIMIZES", "weight": 1, "description": "AI优化沉积优化薄膜质量"},
            {"start_id": "method_061", "end_id": "capability_021", "relationship_type": "ENABLES", "weight": 1, "description": "实时过程控制实现原位监测与控制"},
            {"start_id": "method_062", "end_id": "capability_021", "relationship_type": "ENABLES", "weight": 1, "description": "数字孪生沉积实现过程模拟优化"},

            # 连接复合技术到组成技术
            {"start_id": "method_057", "end_id": "tech_001", "relationship_type": "COMBINES", "weight": 1, "description": "PVD-CVD复合沉积结合PVD技术"},
            {"start_id": "method_057", "end_id": "tech_002", "relationship_type": "COMBINES", "weight": 1, "description": "PVD-CVD复合沉积结合CVD技术"},
            {"start_id": "method_058", "end_id": "tech_009", "relationship_type": "COMBINES", "weight": 1, "description": "电化学-ALD复合技术结合电化学沉积"},
            {"start_id": "method_058", "end_id": "tech_003", "relationship_type": "COMBINES", "weight": 1, "description": "电化学-ALD复合技术结合ALD技术"},
            {"start_id": "method_059", "end_id": "tech_011", "relationship_type": "COMBINES", "weight": 1, "description": "激光-溶液复合沉积结合激光加工"},
            {"start_id": "method_059", "end_id": "tech_004", "relationship_type": "COMBINES", "weight": 1, "description": "激光-溶液复合沉积结合溶液法"},

            # 连接新兴材料到应用领域
            {"start_id": "material_075", "end_id": "structure_020", "relationship_type": "USED_IN", "weight": 1, "description": "黑磷用于二维通道"},
            {"start_id": "material_076", "end_id": "structure_020", "relationship_type": "USED_IN", "weight": 1, "description": "ReS₂用于二维通道"},
            {"start_id": "material_077", "end_id": "structure_020", "relationship_type": "USED_IN", "weight": 1, "description": "PtSe₂用于二维通道"},
            {"start_id": "material_078", "end_id": "structure_020", "relationship_type": "USED_IN", "weight": 1, "description": "Janus二维材料用于二维通道"},
            {"start_id": "material_079", "end_id": "structure_028", "relationship_type": "USED_IN", "weight": 1, "description": "多铁性材料用于自旋阀"},
            {"start_id": "material_080", "end_id": "structure_036", "relationship_type": "USED_IN", "weight": 1, "description": "拓扑绝缘体用于拓扑量子比特"},
            {"start_id": "material_081", "end_id": "structure_035", "relationship_type": "USED_IN", "weight": 1, "description": "Weyl半金属用于自旋轨道耦合器"},
            {"start_id": "material_082", "end_id": "structure_038", "relationship_type": "USED_IN", "weight": 1, "description": "MOF材料用于生物传感器"},
            {"start_id": "material_083", "end_id": "structure_039", "relationship_type": "USED_IN", "weight": 1, "description": "导电聚合物用于柔性电极"},
            {"start_id": "material_084", "end_id": "structure_034", "relationship_type": "USED_IN", "weight": 1, "description": "水凝胶用于可穿戴器件"},
            {"start_id": "material_085", "end_id": "structure_038", "relationship_type": "USED_IN", "weight": 1, "description": "丝素蛋白用于生物传感器"},
            # 新兴技术与反应类型的关系
            {"start_id": "tech_016", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "神经形态计算制造涉及物理过程"},
            {"start_id": "tech_016", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "神经形态计算制造涉及化学过程"},
            {"start_id": "tech_017", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "生物电子集成涉及化学过程"},
            {"start_id": "tech_018", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "可持续绿色制造涉及化学过程"},

            # 新兴技术与能力的关系
            {"start_id": "tech_016", "end_id": "capability_031", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "神经形态计算制造具有高计算效率"},
            {"start_id": "tech_017", "end_id": "capability_032", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "生物电子集成具有高生物信号灵敏度"},
            {"start_id": "tech_019", "end_id": "capability_033", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "极端环境电子制造具有强环境适应性"},
            {"start_id": "tech_018", "end_id": "capability_034", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "可持续绿色制造具有高能量转换效率"},

            # 新兴应用领域与技术的关系
            {"start_id": "tech_016", "end_id": "structure_041", "relationship_type": "USED_FOR", "weight": 1, "description": "神经形态计算制造用于神经形态计算阵列"},
            {"start_id": "tech_017", "end_id": "structure_042", "relationship_type": "USED_FOR", "weight": 1, "description": "生物电子集成用于生物-电子接口"},
            {"start_id": "tech_018", "end_id": "structure_043", "relationship_type": "USED_FOR", "weight": 1, "description": "可持续绿色制造用于能量收集器"},
            {"start_id": "tech_019", "end_id": "structure_044", "relationship_type": "USED_FOR", "weight": 1, "description": "极端环境电子制造用于太赫兹器件"},
            {"start_id": "tech_020", "end_id": "structure_045", "relationship_type": "USED_FOR", "weight": 1, "description": "光子集成制造用于超表面"},

            # 新材料与技术的关系
            {"start_id": "tech_004", "end_id": "material_086", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀有机-无机杂化钙钛矿"},
            {"start_id": "tech_004", "end_id": "material_087", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀共价有机框架"},
            {"start_id": "tech_004", "end_id": "material_088", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长处理液态金属"},
            {"start_id": "tech_003", "end_id": "material_089", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀量子点发光材料"},
            {"start_id": "tech_002", "end_id": "material_090", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长制备多孔硅"},

            # 新参数与材料的关系
            {"start_id": "material_086", "end_id": "parameter_015", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "有机-无机杂化钙钛矿具有可调光学带隙"},
            {"start_id": "material_087", "end_id": "parameter_033", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "共价有机框架具有高比表面积"},
            {"start_id": "material_088", "end_id": "parameter_005", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "液态金属具有高电导率"},
            {"start_id": "material_089", "end_id": "parameter_015", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "量子点发光材料具有尺寸依赖的发光特性"},
            {"start_id": "material_090", "end_id": "parameter_032", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "多孔硅具有可调孔隙率和表面积"},

            # 新设备与方法的关系
            {"start_id": "tech_016", "end_id": "equipment_049", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "神经形态计算制造需要神经形态测试系统"},
            {"start_id": "tech_017", "end_id": "equipment_050", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "生物电子集成需要生物安全沉积系统"},
            {"start_id": "tech_019", "end_id": "equipment_051", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "极端环境电子制造需要太赫兹测试系统"},
            {"start_id": "tech_020", "end_id": "equipment_052", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "光子集成制造需要超表面制造系统"},
            {"start_id": "tech_018", "end_id": "equipment_053", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "可持续绿色制造需要可持续制造评估系统"},

            # 新兴交叉技术关系
            {"start_id": "tech_016", "end_id": "tech_003", "relationship_type": "COMBINES", "weight": 0.8, "description": "神经形态计算制造结合ALD技术"},
            {"start_id": "tech_017", "end_id": "tech_004", "relationship_type": "COMBINES", "weight": 0.8, "description": "生物电子集成结合溶液法技术"},
            {"start_id": "tech_018", "end_id": "tech_002", "relationship_type": "IMPROVES", "weight": 0.7, "description": "可持续绿色制造改进CVD工艺环保性"},
            {"start_id": "tech_019", "end_id": "tech_005", "relationship_type": "SPECIALIZES", "weight": 0.9, "description": "极端环境电子制造专门化外延生长技术"},

            # 制造阶段与新应用领域
            {"start_id": "structure_041", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "神经形态计算阵列制造于前道工艺"},
            {"start_id": "structure_042", "end_id": "stage_004", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "生物-电子接口制造于先进封装阶段"},
            {"start_id": "structure_043", "end_id": "stage_002", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "能量收集器制造于后道工艺"},
            {"start_id": "structure_044", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "太赫兹器件制造于前道工艺"},
            {"start_id": "structure_045", "end_id": "stage_001", "relationship_type": "MANUFACTURED_IN", "weight": 1, "description": "超表面制造于前道工艺"},

            # 参数与能力的关系
            {"start_id": "parameter_043", "end_id": "capability_031", "relationship_type": "QUANTIFIES", "weight": 1, "description": "神经突触权重量化计算效率"},
            {"start_id": "parameter_044", "end_id": "capability_027", "relationship_type": "QUANTIFIES", "weight": 1, "description": "生物兼容性等级量化生物兼容性"},
            {"start_id": "parameter_045", "end_id": "capability_034", "relationship_type": "QUANTIFIES", "weight": 1, "description": "能量收集密度量化能量转换效率"},
            {"start_id": "parameter_046", "end_id": "capability_035", "relationship_type": "QUANTIFIES", "weight": 1, "description": "太赫兹吸收率量化太赫兹响应特性"},

            # 检测设备与新参数
            {"start_id": "equipment_049", "end_id": "parameter_043", "relationship_type": "MEASURES", "weight": 1, "description": "神经形态测试系统测量神经突触权重"},
            {"start_id": "equipment_050", "end_id": "parameter_044", "relationship_type": "MEASURES", "weight": 1, "description": "生物安全沉积系统监测生物兼容性等级"},
            {"start_id": "equipment_051", "end_id": "parameter_046", "relationship_type": "MEASURES", "weight": 1, "description": "太赫兹测试系统测量太赫兹吸收率"},
            {"start_id": "equipment_052", "end_id": "parameter_047", "relationship_type": "MEASURES", "weight": 1, "description": "超表面制造系统监测相位调控精度"},

            # 可持续性关系
            {"start_id": "tech_018", "end_id": "material_087", "relationship_type": "PREFERS_MATERIAL", "weight": 0.8, "description": "可持续绿色制造优选共价有机框架材料"},
            {"start_id": "tech_018", "end_id": "method_028", "relationship_type": "PREFERS_METHOD", "weight": 0.7, "description": "可持续绿色制造优选溶胶-凝胶法"},
            {"start_id": "tech_018", "end_id": "capability_007", "relationship_type": "OPTIMIZES", "weight": 0.9, "description": "可持续绿色制造优化低成本特性"},

            # 极端环境适应性
            {"start_id": "tech_019", "end_id": "material_036", "relationship_type": "PREFERS_MATERIAL", "weight": 0.9, "description": "极端环境电子制造优选SiC材料"},
            {"start_id": "tech_019", "end_id": "material_037", "relationship_type": "PREFERS_MATERIAL", "weight": 0.8, "description": "极端环境电子制造优选金刚石材料"},
            {"start_id": "tech_019", "end_id": "material_071", "relationship_type": "PREFERS_MATERIAL", "weight": 0.7, "description": "极端环境电子制造优选Ga₂O₃材料"},

            # 光子集成关系
            {"start_id": "tech_020", "end_id": "material_050", "relationship_type": "PREFERS_MATERIAL", "weight": 0.9, "description": "光子集成制造优选铌酸锂材料"},
            {"start_id": "tech_020", "end_id": "material_022", "relationship_type": "PREFERS_MATERIAL", "weight": 0.8, "description": "光子集成制造优选硅材料"},
            {"start_id": "tech_020", "end_id": "method_019", "relationship_type": "PREFERS_METHOD", "weight": 0.7, "description": "光子集成制造优选MBE方法"},

            # 补充技术发展趋势关系
            {"start_id": "tech_016", "end_id": "tech_015", "relationship_type": "EVOLVES_TO", "weight": 0.8, "description": "智能沉积技术向神经形态计算制造演进"},
            {"start_id": "tech_017", "end_id": "tech_004", "relationship_type": "EVOLVES_FROM", "weight": 0.7, "description": "生物电子集成从溶液法技术演进而来"},
            {"start_id": "tech_018", "end_id": "tech_002", "relationship_type": "GREEN_VERSION_OF", "weight": 0.9, "description": "可持续绿色制造是CVD的环保版本"},

            # 材料性能优化关系
            {"start_id": "material_086", "end_id": "material_044", "relationship_type": "IMPROVES", "weight": 0.8, "description": "有机-无机杂化钙钛矿改进传统钙钛矿稳定性"},
            {"start_id": "material_087", "end_id": "material_082", "relationship_type": "ORGANIC_VERSION_OF", "weight": 0.7, "description": "共价有机框架是有机版本的MOF材料"},
            {"start_id": "material_088", "end_id": "material_002", "relationship_type": "FLEXIBLE_ALTERNATIVE", "weight": 0.6, "description": "液态金属是铜的柔性替代材料"},

            # 应用领域交叉关系
            {"start_id": "structure_041", "end_id": "structure_031", "relationship_type": "INTEGRATES", "weight": 0.9, "description": "神经形态计算阵列集成神经形态器件"},
            {"start_id": "structure_042", "end_id": "structure_038", "relationship_type": "ENHANCES", "weight": 0.8, "description": "生物-电子接口增强生物传感器性能"},
            {"start_id": "structure_043", "end_id": "structure_034", "relationship_type": "POWERS", "weight": 0.7, "description": "能量收集器为可穿戴器件供电"},

            # 工艺协同关系
            {"start_id": "method_009", "end_id": "method_060", "relationship_type": "BENEFITS_FROM", "weight": 0.8, "description": "热ALD受益于AI优化沉积"},
            {"start_id": "method_015", "end_id": "method_058", "relationship_type": "EVOLVES_TO", "weight": 0.7, "description": "电化学沉积演进为电化学-ALD复合技术"},
            {"start_id": "method_001", "end_id": "method_057", "relationship_type": "COMBINES_INTO", "weight": 0.9, "description": "溅射技术结合形成PVD-CVD复合沉积"},
            {"start_id": "tech_008", "end_id": "action_004", "relationship_type": "HAS_ACTION", "weight": 1, "description": "量子器件制造涉及热过程"},
            {"start_id": "tech_016", "end_id": "action_004", "relationship_type": "HAS_ACTION", "weight": 1, "description": "神经形态计算制造涉及热过程"},

            # 处理 Technology 孤立节点
            {"start_id": "tech_012", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "纳米压印技术属于物理过程"},
            {"start_id": "method_039", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "纳米压印属于纳米压印技术"},
            {"start_id": "method_051", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "热纳米压印属于纳米压印技术"},
            {"start_id": "method_052", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "紫外纳米压印属于纳米压印技术"},
            {"start_id": "method_053", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "软纳米压印属于纳米压印技术"},

            {"start_id": "tech_013", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "自组装技术属于化学过程"},
            {"start_id": "method_030", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "分子自组装属于自组装技术"},
            {"start_id": "method_054", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "嵌段共聚物自组装属于自组装技术"},
            {"start_id": "method_055", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "DNA引导自组装属于自组装技术"},
            {"start_id": "method_056", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "胶体晶体自组装属于自组装技术"},

            {"start_id": "tech_014", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "混合沉积技术涉及物理过程"},
            {"start_id": "tech_014", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "混合沉积技术涉及化学过程"},
            {"start_id": "method_057", "end_id": "tech_014", "relationship_type": "BELONGS_TO", "weight": 1, "description": "PVD-CVD复合沉积属于混合沉积技术"},
            {"start_id": "method_058", "end_id": "tech_014", "relationship_type": "BELONGS_TO", "weight": 1, "description": "电化学-ALD复合技术属于混合沉积技术"},
            {"start_id": "method_059", "end_id": "tech_014", "relationship_type": "BELONGS_TO", "weight": 1, "description": "激光-溶液复合沉积属于混合沉积技术"},

            {"start_id": "tech_015", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "智能沉积技术涉及物理过程"},
            {"start_id": "tech_015", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "智能沉积技术涉及化学过程"},
            {"start_id": "method_060", "end_id": "tech_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "AI优化沉积属于智能沉积技术"},
            {"start_id": "method_061", "end_id": "tech_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "实时过程控制属于智能沉积技术"},
            {"start_id": "method_062", "end_id": "tech_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "数字孪生沉积属于智能沉积技术"},

            {"start_id": "tech_016", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "神经形态计算制造涉及物理过程"},
            {"start_id": "tech_016", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "神经形态计算制造涉及化学过程"},
            {"start_id": "tech_016", "end_id": "structure_031", "relationship_type": "USED_FOR", "weight": 1, "description": "神经形态计算制造用于神经形态器件"},
            {"start_id": "tech_016", "end_id": "structure_037", "relationship_type": "USED_FOR", "weight": 1, "description": "神经形态计算制造用于神经形态突触"},
            {"start_id": "tech_016", "end_id": "structure_041", "relationship_type": "USED_FOR", "weight": 1, "description": "神经形态计算制造用于神经形态计算阵列"},

            {"start_id": "tech_017", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "生物电子集成涉及化学过程"},
            {"start_id": "tech_017", "end_id": "structure_038", "relationship_type": "USED_FOR", "weight": 1, "description": "生物电子集成用于生物传感器"},
            {"start_id": "tech_017", "end_id": "structure_042", "relationship_type": "USED_FOR", "weight": 1, "description": "生物电子集成用于生物-电子接口"},
            {"start_id": "tech_017", "end_id": "material_083", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "生物电子集成使用导电聚合物"},
            {"start_id": "tech_017", "end_id": "material_085", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "生物电子集成使用丝素蛋白"},

            {"start_id": "tech_018", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "可持续绿色制造涉及化学过程"},
            {"start_id": "tech_018", "end_id": "capability_007", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "可持续绿色制造具有低成本特点"},
            {"start_id": "tech_018", "end_id": "material_087", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "可持续绿色制造使用共价有机框架"},
            {"start_id": "tech_018", "end_id": "method_028", "relationship_type": "USES_METHOD", "weight": 1, "description": "可持续绿色制造使用溶胶-凝胶法"},

            {"start_id": "tech_019", "end_id": "action_004", "relationship_type": "HAS_ACTION", "weight": 1, "description": "极端环境电子制造涉及热过程"},
            {"start_id": "tech_019", "end_id": "material_036", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "极端环境电子制造使用SiC"},
            {"start_id": "tech_019", "end_id": "material_037", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "极端环境电子制造使用金刚石"},
            {"start_id": "tech_019", "end_id": "structure_044", "relationship_type": "USED_FOR", "weight": 1, "description": "极端环境电子制造用于太赫兹器件"},

            {"start_id": "tech_020", "end_id": "action_001", "relationship_type": "HAS_ACTION", "weight": 1, "description": "光子集成制造涉及物理过程"},
            {"start_id": "tech_020", "end_id": "action_002", "relationship_type": "HAS_ACTION", "weight": 1, "description": "光子集成制造涉及化学过程"},
            {"start_id": "tech_020", "end_id": "material_050", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "光子集成制造使用铌酸锂"},
            {"start_id": "tech_020", "end_id": "structure_030", "relationship_type": "USED_FOR", "weight": 1, "description": "光子集成制造用于光子集成电路"},
            {"start_id": "tech_020", "end_id": "structure_045", "relationship_type": "USED_FOR", "weight": 1, "description": "光子集成制造用于超表面"},

            # 处理 Method 孤立节点
            {"start_id": "method_053", "end_id": "tech_012", "relationship_type": "BELONGS_TO", "weight": 1, "description": "软纳米压印属于纳米压印技术"},
            {"start_id": "method_053", "end_id": "equipment_034", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "软纳米压印需要纳米压印系统"},
            {"start_id": "method_053", "end_id": "capability_019", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "软纳米压印具有纳米级图案化能力"},

            {"start_id": "method_055", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "DNA引导自组装属于自组装技术"},
            {"start_id": "method_055", "end_id": "equipment_022", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "DNA引导自组装需要分子自组装系统"},
            {"start_id": "method_055", "end_id": "capability_019", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "DNA引导自组装具有纳米级图案化能力"},

            {"start_id": "method_056", "end_id": "tech_013", "relationship_type": "BELONGS_TO", "weight": 1, "description": "胶体晶体自组装属于自组装技术"},
            {"start_id": "method_056", "end_id": "equipment_022", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "胶体晶体自组装需要分子自组装系统"},
            {"start_id": "method_056", "end_id": "structure_022", "relationship_type": "USED_FOR", "weight": 1, "description": "胶体晶体自组装用于光子晶体"},

            {"start_id": "method_058", "end_id": "tech_014", "relationship_type": "BELONGS_TO", "weight": 1, "description": "电化学-ALD复合技术属于混合沉积技术"},
            {"start_id": "method_058", "end_id": "tech_009", "relationship_type": "COMBINES", "weight": 1, "description": "电化学-ALD复合技术结合电化学沉积"},
            {"start_id": "method_058", "end_id": "tech_003", "relationship_type": "COMBINES", "weight": 1, "description": "电化学-ALD复合技术结合ALD技术"},

            {"start_id": "method_059", "end_id": "tech_014", "relationship_type": "BELONGS_TO", "weight": 1, "description": "激光-溶液复合沉积属于混合沉积技术"},
            {"start_id": "method_059", "end_id": "tech_011", "relationship_type": "COMBINES", "weight": 1, "description": "激光-溶液复合沉积结合激光加工"},
            {"start_id": "method_059", "end_id": "tech_004", "relationship_type": "COMBINES", "weight": 1, "description": "激光-溶液复合沉积结合溶液法"},

            {"start_id": "method_061", "end_id": "tech_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "实时过程控制属于智能沉积技术"},
            {"start_id": "method_061", "end_id": "capability_021", "relationship_type": "ENABLES", "weight": 1, "description": "实时过程控制实现原位监测与控制"},
            {"start_id": "method_061", "end_id": "equipment_027", "relationship_type": "USES_EQUIPMENT", "weight": 1, "description": "实时过程控制使用原位监测系统"},

            {"start_id": "method_062", "end_id": "tech_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "数字孪生沉积属于智能沉积技术"},
            {"start_id": "method_062", "end_id": "capability_021", "relationship_type": "ENABLES", "weight": 1, "description": "数字孪生沉积实现过程模拟优化"},
            {"start_id": "method_062", "end_id": "method_060", "relationship_type": "COMBINES_WITH", "weight": 1, "description": "数字孪生沉积与AI优化沉积结合"},

            # 处理 SubMethod 孤立节点
            {"start_id": "submethod_011", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "等离子体增强溅射属于溅射方法"},
            {"start_id": "submethod_011", "end_id": "capability_001", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "等离子体增强溅射具有高沉积速率"},
            {"start_id": "submethod_011", "end_id": "tech_010", "relationship_type": "USES_TECH", "weight": 1, "description": "等离子体增强溅射使用等离子体技术"},

            {"start_id": "submethod_012", "end_id": "method_009", "relationship_type": "BELONGS_TO", "weight": 1, "description": "激光辅助ALD属于热ALD方法"},
            {"start_id": "submethod_012", "end_id": "tech_011", "relationship_type": "USES_TECH", "weight": 1, "description": "激光辅助ALD使用激光加工技术"},
            {"start_id": "submethod_012", "end_id": "capability_003", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "激光辅助ALD具有低温工艺特点"},

            {"start_id": "submethod_013", "end_id": "method_001", "relationship_type": "BELONGS_TO", "weight": 1, "description": "磁场辅助沉积属于溅射方法"},
            {"start_id": "submethod_013", "end_id": "capability_005", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "磁场辅助沉积改善薄膜质量"},
            {"start_id": "submethod_013", "end_id": "submethod_003", "relationship_type": "IMPROVES", "weight": 1, "description": "磁场辅助沉积改进磁控溅射"},

            {"start_id": "submethod_014", "end_id": "method_015", "relationship_type": "BELONGS_TO", "weight": 1, "description": "超声辅助沉积属于电化学沉积方法"},
            {"start_id": "submethod_014", "end_id": "capability_006", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "超声辅助沉积改善保形性"},
            {"start_id": "submethod_014", "end_id": "parameter_003", "relationship_type": "AFFECTS_PARAMETER", "weight": 1, "description": "超声辅助沉积影响表面粗糙度"},

            # 处理 Material 孤立节点
            {"start_id": "tech_005", "end_id": "material_072", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀β-Ga₂O₃"},
            {"start_id": "material_072", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "β-Ga₂O₃具有4.7-4.9eV带隙"},
            {"start_id": "material_072", "end_id": "parameter_013", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "β-Ga₂O₃具有高击穿场强"},

            {"start_id": "tech_004", "end_id": "material_073", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀ZnO纳米线"},
            {"start_id": "material_073", "end_id": "structure_019", "relationship_type": "USED_IN", "weight": 1, "description": "ZnO纳米线用于纳米线结构"},
            {"start_id": "material_073", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ZnO纳米线具有3.37eV带隙"},

            {"start_id": "tech_002", "end_id": "material_074", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长沉淀SiC纳米管"},
            {"start_id": "material_074", "end_id": "structure_019", "relationship_type": "USED_IN", "weight": 1, "description": "SiC纳米管用于纳米线结构"},
            {"start_id": "material_074", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "SiC纳米管具有2.4-3.3eV带隙"},

            {"start_id": "tech_003", "end_id": "material_076", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀ReS₂"},
            {"start_id": "material_076", "end_id": "structure_020", "relationship_type": "USED_IN", "weight": 1, "description": "ReS₂用于二维通道"},
            {"start_id": "material_076", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "ReS₂具有1.5eV带隙"},

            {"start_id": "tech_003", "end_id": "material_077", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀PtSe₂"},
            {"start_id": "material_077", "end_id": "structure_020", "relationship_type": "USED_IN", "weight": 1, "description": "PtSe₂用于二维通道"},
            {"start_id": "material_077", "end_id": "parameter_011", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "PtSe₂具有1.2eV带隙"},

            {"start_id": "tech_003", "end_id": "material_078", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀Janus二维材料"},
            {"start_id": "material_078", "end_id": "structure_020", "relationship_type": "USED_IN", "weight": 1, "description": "Janus二维材料用于二维通道"},
            {"start_id": "material_078", "end_id": "capability_009", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "Janus二维材料具有区域控制特性"},

            {"start_id": "tech_005", "end_id": "material_079", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀多铁性材料"},
            {"start_id": "material_079", "end_id": "structure_028", "relationship_type": "USED_IN", "weight": 1, "description": "多铁性材料用于自旋阀"},
            {"start_id": "material_079", "end_id": "parameter_022", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "多铁性材料具有铁电特性"},

            {"start_id": "tech_005", "end_id": "material_080", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀拓扑绝缘体"},
            {"start_id": "material_080", "end_id": "structure_036", "relationship_type": "USED_IN", "weight": 1, "description": "拓扑绝缘体用于拓扑量子比特"},
            {"start_id": "material_080", "end_id": "parameter_036", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "拓扑绝缘体具有拓扑不变量"},

            {"start_id": "tech_005", "end_id": "material_081", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "外延生长擅长沉淀Weyl半金属"},
            {"start_id": "material_081", "end_id": "structure_035", "relationship_type": "USED_IN", "weight": 1, "description": "Weyl半金属用于自旋轨道耦合器"},
            {"start_id": "material_081", "end_id": "parameter_036", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Weyl半金属具有拓扑不变量"},

            {"start_id": "tech_004", "end_id": "material_082", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀MOF材料"},
            {"start_id": "material_082", "end_id": "structure_038", "relationship_type": "USED_IN", "weight": 1, "description": "MOF材料用于生物传感器"},
            {"start_id": "material_082", "end_id": "parameter_033", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "MOF材料具有高比表面积"},

            {"start_id": "tech_004", "end_id": "material_084", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀水凝胶"},
            {"start_id": "material_084", "end_id": "structure_034", "relationship_type": "USED_IN", "weight": 1, "description": "水凝胶用于可穿戴器件"},
            {"start_id": "material_084", "end_id": "parameter_037", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "水凝胶具有生物兼容性"},

            {"start_id": "tech_004", "end_id": "material_086", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀有机-无机杂化钙钛矿"},
            {"start_id": "material_086", "end_id": "structure_033", "relationship_type": "USED_IN", "weight": 1, "description": "有机-无机杂化钙钛矿用于透明电子"},
            {"start_id": "material_086", "end_id": "parameter_015", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "有机-无机杂化钙钛矿具有可调光学带隙"},

            {"start_id": "tech_004", "end_id": "material_087", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长沉淀共价有机框架"},
            {"start_id": "material_087", "end_id": "structure_038", "relationship_type": "USED_IN", "weight": 1, "description": "共价有机框架用于生物传感器"},
            {"start_id": "material_087", "end_id": "parameter_033", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "共价有机框架具有高比表面积"},

            {"start_id": "tech_004", "end_id": "material_088", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "溶液法擅长处理液态金属"},
            {"start_id": "material_088", "end_id": "structure_039", "relationship_type": "USED_IN", "weight": 1, "description": "液态金属用于柔性电极"},
            {"start_id": "material_088", "end_id": "parameter_005", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "液态金属具有高电导率"},

            {"start_id": "tech_003", "end_id": "material_089", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "ALD擅长沉淀量子点发光材料"},
            {"start_id": "material_089", "end_id": "structure_021", "relationship_type": "USED_IN", "weight": 1, "description": "量子点发光材料用于量子点"},
            {"start_id": "material_089", "end_id": "parameter_015", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "量子点发光材料具有尺寸依赖发光特性"},

            {"start_id": "tech_002", "end_id": "material_090", "relationship_type": "EFFICIENT_PRECIPITATION", "weight": 1, "description": "CVD擅长制备多孔硅"},
            {"start_id": "material_090", "end_id": "structure_038", "relationship_type": "USED_IN", "weight": 1, "description": "多孔硅用于生物传感器"},
            {"start_id": "material_090", "end_id": "parameter_032", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "多孔硅具有可调孔隙率"},

            # 处理 Capability 孤立节点
            {"start_id": "tech_008", "end_id": "capability_024", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "量子器件制造具有量子相干控制能力"},
            {"start_id": "capability_024", "end_id": "parameter_029", "relationship_type": "RELATED_TO", "weight": 1, "description": "量子相干控制与相干时间相关"},

            {"start_id": "tech_007", "end_id": "capability_025", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "异质集成具有自旋极化控制能力"},
            {"start_id": "capability_025", "end_id": "parameter_030", "relationship_type": "RELATED_TO", "weight": 1, "description": "自旋极化控制与自旋弛豫时间相关"},

            {"start_id": "tech_007", "end_id": "capability_026", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "异质集成具有拓扑态调控能力"},
            {"start_id": "capability_026", "end_id": "parameter_036", "relationship_type": "RELATED_TO", "weight": 1, "description": "拓扑态调控与拓扑不变量相关"},

            {"start_id": "tech_004", "end_id": "capability_028", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有可降解性"},
            {"start_id": "capability_028", "end_id": "parameter_038", "relationship_type": "RELATED_TO", "weight": 1, "description": "可降解性与降解速率相关"},

            {"start_id": "tech_004", "end_id": "capability_029", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有自修复能力"},
            {"start_id": "capability_029", "end_id": "parameter_039", "relationship_type": "RELATED_TO", "weight": 1, "description": "自修复能力与自修复效率相关"},

            {"start_id": "tech_004", "end_id": "capability_030", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "溶液法具有形状记忆能力"},
            {"start_id": "capability_030", "end_id": "material_084", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "形状记忆能力表征水凝胶材料"},

            {"start_id": "tech_016", "end_id": "capability_031", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "神经形态计算制造具有高计算效率"},
            {"start_id": "capability_031", "end_id": "parameter_043", "relationship_type": "QUANTIFIES", "weight": 1, "description": "神经形态计算效率由突触权重量化"},

            {"start_id": "tech_017", "end_id": "capability_032", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "生物电子集成具有高生物信号灵敏度"},
            {"start_id": "capability_032", "end_id": "structure_038", "relationship_type": "IMPORTANT_FOR", "weight": 1, "description": "生物信号灵敏度对生物传感器重要"},

            {"start_id": "tech_019", "end_id": "capability_033", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "极端环境电子制造具有强环境适应性"},
            {"start_id": "capability_033", "end_id": "material_036", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "环境适应性表征SiC材料"},

            {"start_id": "tech_018", "end_id": "capability_034", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "可持续绿色制造具有高能量转换效率"},
            {"start_id": "capability_034", "end_id": "parameter_045", "relationship_type": "QUANTIFIES", "weight": 1, "description": "能量转换效率由能量收集密度量化"},

            {"start_id": "tech_019", "end_id": "capability_035", "relationship_type": "HAS_ABILITY", "weight": 1, "description": "极端环境电子制造具有太赫兹响应特性"},
            {"start_id": "capability_035", "end_id": "parameter_046", "relationship_type": "QUANTIFIES", "weight": 1, "description": "太赫兹响应特性由太赫兹吸收率量化"},

            # 处理 Equipment 孤立节点
            {"start_id": "method_045", "end_id": "equipment_037", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "激光化学气相沉积需要LCVD系统"},
            {"start_id": "equipment_037", "end_id": "tech_002", "relationship_type": "USED_FOR", "weight": 1, "description": "LCVD系统用于CVD技术"},

            {"start_id": "method_046", "end_id": "equipment_038", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "电子束诱导沉积需要EBID系统"},
            {"start_id": "equipment_038", "end_id": "tech_001", "relationship_type": "USED_FOR", "weight": 1, "description": "EBID系统用于PVD技术"},

            {"start_id": "method_047", "end_id": "equipment_039", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "离子束沉积需要IBD系统"},
            {"start_id": "equipment_039", "end_id": "tech_001", "relationship_type": "USED_FOR", "weight": 1, "description": "IBD系统用于PVD技术"},

            {"start_id": "method_048", "end_id": "equipment_040", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "团簇束沉积需要CBD系统"},
            {"start_id": "equipment_040", "end_id": "tech_001", "relationship_type": "USED_FOR", "weight": 1, "description": "CBD系统用于PVD技术"},

            {"start_id": "method_051", "end_id": "equipment_043", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "热纳米压印需要飞秒激光系统"},
            {"start_id": "equipment_043", "end_id": "tech_011", "relationship_type": "USED_FOR", "weight": 1, "description": "飞秒激光系统用于激光加工技术"},

            {"start_id": "tech_003", "end_id": "equipment_044", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "ALD需要低温沉积系统"},
            {"start_id": "equipment_044", "end_id": "capability_003", "relationship_type": "ENABLES", "weight": 1, "description": "低温沉积系统实现低温工艺"},

            {"start_id": "method_060", "end_id": "equipment_045", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "AI优化沉积需要超高真空互联系统"},
            {"start_id": "equipment_045", "end_id": "tech_015", "relationship_type": "USED_FOR", "weight": 1, "description": "超高真空互联系统用于智能沉积技术"},

            {"start_id": "tech_008", "end_id": "equipment_046", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "量子器件制造需要量子比特测试系统"},
            {"start_id": "equipment_046", "end_id": "parameter_029", "relationship_type": "MEASURES", "weight": 1, "description": "量子比特测试系统测量相干时间"},

            {"start_id": "tech_007", "end_id": "equipment_047", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "异质集成需要自旋测量系统"},
            {"start_id": "equipment_047", "end_id": "parameter_030", "relationship_type": "MEASURES", "weight": 1, "description": "自旋测量系统测量自旋弛豫时间"},

            {"start_id": "tech_017", "end_id": "equipment_048", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "生物电子集成需要生物兼容沉积系统"},
            {"start_id": "equipment_048", "end_id": "capability_027", "relationship_type": "ENABLES", "weight": 1, "description": "生物兼容沉积系统实现生物兼容性"},

            {"start_id": "tech_016", "end_id": "equipment_049", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "神经形态计算制造需要神经形态测试系统"},
            {"start_id": "equipment_049", "end_id": "parameter_043", "relationship_type": "MEASURES", "weight": 1, "description": "神经形态测试系统测量突触权重"},

            {"start_id": "tech_017", "end_id": "equipment_050", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "生物电子集成需要生物安全沉积系统"},
            {"start_id": "equipment_050", "end_id": "parameter_044", "relationship_type": "MONITORS", "weight": 1, "description": "生物安全沉积系统监测生物兼容性"},

            {"start_id": "tech_019", "end_id": "equipment_051", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "极端环境电子制造需要太赫兹测试系统"},
            {"start_id": "equipment_051", "end_id": "parameter_046", "relationship_type": "MEASURES", "weight": 1, "description": "太赫兹测试系统测量太赫兹吸收率"},

            {"start_id": "tech_020", "end_id": "equipment_052", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "光子集成制造需要超表面制造系统"},
            {"start_id": "equipment_052", "end_id": "parameter_047", "relationship_type": "MONITORS", "weight": 1, "description": "超表面制造系统监测相位调控精度"},

            {"start_id": "tech_018", "end_id": "equipment_053", "relationship_type": "NEED_EQUIPMENT", "weight": 1, "description": "可持续绿色制造需要可持续制造评估系统"},
            {"start_id": "equipment_053", "end_id": "capability_007", "relationship_type": "EVALUATES", "weight": 1, "description": "可持续制造评估系统评估成本效益"},

            # 处理 Parameter 孤立节点
            {"start_id": "material_070", "end_id": "parameter_031", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "YBCO具有超导转变温度"},
            {"start_id": "parameter_031", "end_id": "structure_027", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "超导转变温度表征量子比特"},

            {"start_id": "material_002", "end_id": "parameter_032", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Cu具有载流子浓度"},
            {"start_id": "material_022", "end_id": "parameter_032", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "Si具有载流子浓度"},
            {"start_id": "parameter_032", "end_id": "parameter_005", "relationship_type": "AFFECTS", "weight": 1, "description": "载流子浓度影响电阻率"},

            {"start_id": "material_005", "end_id": "parameter_033", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "SiO₂具有薄膜密度"},
            {"start_id": "material_007", "end_id": "parameter_033", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "HfO₂具有薄膜密度"},
            {"start_id": "tech_001", "end_id": "parameter_033", "relationship_type": "AFFECTS_PARAMETER", "weight": 1, "description": "PVD工艺影响薄膜密度"},

            {"start_id": "structure_027", "end_id": "parameter_034", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "量子比特具有量子相干时间"},
            {"start_id": "parameter_034", "end_id": "capability_024", "relationship_type": "QUANTIFIES", "weight": 1, "description": "量子相干时间量化量子相干控制"},

            {"start_id": "structure_028", "end_id": "parameter_035", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "自旋阀具有自旋弛豫时间"},
            {"start_id": "parameter_035", "end_id": "capability_025", "relationship_type": "QUANTIFIES", "weight": 1, "description": "自旋弛豫时间量化自旋极化控制"},

            {"start_id": "material_080", "end_id": "parameter_036", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "拓扑绝缘体具有拓扑不变量"},
            {"start_id": "parameter_036", "end_id": "capability_026", "relationship_type": "QUANTIFIES", "weight": 1, "description": "拓扑不变量量化拓扑态调控"},

            {"start_id": "material_083", "end_id": "parameter_037", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "导电聚合物具有生物兼容性指数"},
            {"start_id": "parameter_037", "end_id": "capability_027", "relationship_type": "QUANTIFIES", "weight": 1, "description": "生物兼容性指数量化生物兼容性"},

            {"start_id": "material_084", "end_id": "parameter_038", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "水凝胶具有降解速率"},
            {"start_id": "parameter_038", "end_id": "capability_028", "relationship_type": "QUANTIFIES", "weight": 1, "description": "降解速率量化可降解性"},

            {"start_id": "material_084", "end_id": "parameter_039", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "水凝胶具有自修复效率"},
            {"start_id": "parameter_039", "end_id": "capability_029", "relationship_type": "QUANTIFIES", "weight": 1, "description": "自修复效率量化自修复能力"},

            {"start_id": "material_042", "end_id": "parameter_040", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "磁性材料具有铁磁矫顽力"},
            {"start_id": "parameter_040", "end_id": "structure_028", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "铁磁矫顽力表征自旋阀"},

            {"start_id": "material_042", "end_id": "parameter_041", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "磁性材料具有磁致伸缩系数"},
            {"start_id": "parameter_041", "end_id": "structure_028", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "磁致伸缩系数表征自旋阀"},

            {"start_id": "material_042", "end_id": "parameter_042", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "磁性材料具有铁磁居里温度"},
            {"start_id": "parameter_042", "end_id": "structure_028", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "铁磁居里温度表征自旋阀"},

            {"start_id": "structure_037", "end_id": "parameter_043", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "神经形态突触具有神经突触权重"},
            {"start_id": "parameter_043", "end_id": "capability_031", "relationship_type": "QUANTIFIES", "weight": 1, "description": "神经突触权重量化计算效率"},

            {"start_id": "material_083", "end_id": "parameter_044", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "导电聚合物具有生物兼容性等级"},
            {"start_id": "parameter_044", "end_id": "capability_027", "relationship_type": "QUANTIFIES", "weight": 1, "description": "生物兼容性等级量化生物兼容性"},

            {"start_id": "structure_043", "end_id": "parameter_045", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "能量收集器具有能量收集密度"},
            {"start_id": "parameter_045", "end_id": "capability_034", "relationship_type": "QUANTIFIES", "weight": 1, "description": "能量收集密度量化能量转换效率"},

            {"start_id": "structure_044", "end_id": "parameter_046", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "太赫兹器件具有太赫兹吸收率"},
            {"start_id": "parameter_046", "end_id": "capability_035", "relationship_type": "QUANTIFIES", "weight": 1, "description": "太赫兹吸收率量化太赫兹响应特性"},

            {"start_id": "structure_045", "end_id": "parameter_047", "relationship_type": "HAS_PARAMETER", "weight": 1, "description": "超表面具有相位调控精度"},
            {"start_id": "parameter_047", "end_id": "tech_020", "relationship_type": "CHARACTERIZES", "weight": 1, "description": "相位调控精度表征光子集成制造"},
        
            {"start_id": "tech_021", "end_id": "method_066", "relationship_type": "HAS_METHOD", "weight": 1, "description": "物理气相沉积通过蒸发等方式实现。"},
            {"start_id": "tech_021", "end_id": "method_001", "relationship_type": "HAS_METHOD", "weight": 1, "description": "物理气相沉积通过溅射等方式实现。"},
            {"start_id": "tech_001", "end_id": "submethod_003", "relationship_type": "HAS_SUBMETHOD", "weight": 1, "description": "PVD工艺包含磁控溅射等方法。"},
            {"start_id": "tech_001", "end_id": "structure_046", "relationship_type": "USED_FOR", "weight": 1, "description": "PVD工艺广泛用于金属互连层的制备。"},
            {"start_id": "tech_001", "end_id": "structure_047", "relationship_type": "USED_FOR", "weight": 1, "description": "PVD工艺广泛用于屏障层的制备。"},
            {"start_id": "tech_002", "end_id": "structure_010", "relationship_type": "USED_FOR", "weight": 1, "description": "CVD工艺是沉积介质层的关键技术。"},
            {"start_id": "tech_002", "end_id": "structure_001", "relationship_type": "USED_FOR", "weight": 1, "description": "CVD工艺是沉积多晶硅栅极的关键技术。"},
            {"start_id": "tech_023", "end_id": "structure_048", "relationship_type": "USED_FOR", "weight": 1, "description": "原子层沉积适用于高深宽比结构中的沉积。"},
            {"start_id": "tech_023", "end_id": "tech_022", "relationship_type": "IS_ADVANCED_FORM_OF", "weight": 1, "description": "原子层沉积是化学气相沉积的进阶形式。"},]
