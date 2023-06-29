import os

os.mkdir("dxg_no_184")
os.mkdir("dxg_no_mdr1")
os.mkdir("dxg_no_184_nor_mdr1")

alias_set_lookup = {
  "0": ["set1_c", "dxg_no_184"],
  "1": ["set9_c", "dxg_no_184"],
  "2": ["set1_ac", "dxg_no_184"],
  "3": ["set9_ac", "dxg_no_184"],
  "4": ["set1_m", "dxg_no_184"],
  "5": ["set9_m", "dxg_no_184"],
  "6": ["set3_c", "dxg_no_184"],
  "7": ["set11_c", "dxg_no_184"],
  "8": ["set3_ac", "dxg_no_184"],
  "9": ["set11_ac", "dxg_no_184"],
  "10": ["set3_m", "dxg_no_184"],
  "11": ["set11_m", "dxg_no_184"],
  "12": ["set1_c", "dxg_no_184"],
  "13": ["set9_c", "dxg_no_mdr1"],
  "14": ["set1_ac", "dxg_no_184"],
  "15": ["set9_ac", "dxg_no_mdr1"],
  "16": ["set1_m", "dxg_no_184"],
  "17": ["set9_m", "dxg_no_mdr1"],
  "18": ["set3_c","dxg_no_mdr1"],
  "19": ["set11_c","dxg_no_mdr1"],
  "20": ["set3_ac","dxg_no_mdr1"],
  "21": ["set11_ac","dxg_no_mdr1"],
  "22": ["set3_m","dxg_no_mdr1"],
  "23": ["set11_m","dxg_no_mdr1"],
  "24": ["set1_c","dxg_no_184_nor_mdr1"],
  "25": ["set9_c","dxg_no_184_nor_mdr1"],
  "26": ["set1_ac","dxg_no_184_nor_mdr1"],
  "27": ["set9_ac","dxg_no_184_nor_mdr1"],
  "28": ["set1_m","dxg_no_184_nor_mdr1"],
  "29": ["set9_m","dxg_no_184_nor_mdr1"],
  "30": ["set3_c","dxg_no_184_nor_mdr1"],
  "31": ["set11_c","dxg_no_184_nor_mdr1"],
  "32": ["set3_ac","dxg_no_184_nor_mdr1"],
  "33": ["set11_ac","dxg_no_184_nor_mdr1"],
  "34": ["set3_m","dxg_no_184_nor_mdr1"],
  "35": ["set11_m","dxg_no_184_nor_mdr1"],
}

for i in range(36):
  filename, dirname = alias_set_lookup[str(i)]
  os.rename(f'{i}.yml', f'{dirname}/{filename}.yml')