# -*- coding: utf-8 -*-
import sys


class LanguageGenerator(object):

    # 3クラスお試し用URL
    URL_DICT = {'足が悪い': ['https://healthrent.duskin.jp/products/hokouhojyo/B-4-24/index.html?link=se_colum_pro_in',
                             'https://www.cainz.com/shop/g/g4936695745505/?utm_content=85&utm_term=&utm_medium=cpc&utm_source=google&utm_campaign=hl_mi_di_al_00_ssc&gclid=Cj0KCQjw_dWGBhDAARIsAMcYuJypt8ejxUrpWKGwR_EBf-6N57I7wlgv8uiVk60nVCDc7UWQ6Y7v51MaAlFZEALw_wcB'],
                '耳が遠い': ['https://www.amazon.co.jp/%E3%82%AA%E3%83%A0%E3%83%AD%E3%83%B3-OMRON-AK-15-%E3%80%90%E9%9D%9E%E8%AA%B2%E7%A8%8E%E3%80%91%E3%82%AA%E3%83%A0%E3%83%AD%E3%83%B3-%E3%82%A4%E3%83%A4%E3%83%A1%E3%82%A4%E3%83%88%E3%83%87%E3%82%B8%E3%82%BF%E3%83%ABAK-15/dp/B01L8CRZL0/ref=asc_df_B01L8CRZL0/?tag=jpgo-22&linkCode=df0&hvadid=218119604762&hvpos=&hvnetw=g&hvrand=10982551009666025837&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1009337&hvtargid=pla-409814589346&psc=1',
                             'https://www.yodobashi.com/product/000000224701012473/?gad1=&gad2=g&gad3=&gad4=452596090545&gad5=15771747885033500943&gad6=&gclid=Cj0KCQjw_dWGBhDAARIsAMcYuJxF4hc65OEa-q1RRTmdr0xQvLwp_bUkSu40q1GPVfT104uWjniSd84aAmBvEALw_wcB&xfr=pla'],
                '認知症': ['https://www.amazon.co.jp/Romi-%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88-ROMI-P02-%E9%80%9A%E5%B8%B8%E8%B2%A9%E5%A3%B2-%E3%83%9E%E3%83%83%E3%83%88%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88/dp/B08H2HL2J7/ref=asc_df_B08H2HL2J7/?tag=jpgo-22&linkCode=df0&hvadid=342578596485&hvpos=&hvnetw=g&hvrand=8439001825582924048&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1009337&hvtargid=pla-1146895915392&psc=1&tag=&ref=&adgrpid=71561406449&hvpone=&hvptwo=&hvadid=342578596485&hvpos=&hvnetw=g&hvrand=8439001825582924048&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1009337&hvtargid=pla-1146895915392',
                           'https://item.rakuten.co.jp/monorogu/php82190/?gclid=Cj0KCQjw_dWGBhDAARIsAMcYuJzP7DBR33yT7dSmBux-8DGF9J91TAWPwhaZPdyx31UrGIO3bZSlEjEaAleSEALw_wcB&scid=af_pc_etc&sc2id=af_113_0_10001868&icm_agid=54982841894&icm_cid=1425341487&icm_acid=834-739-7270&gclid=Cj0KCQjw_dWGBhDAARIsAMcYuJzP7DBR33yT7dSmBux-8DGF9J91TAWPwhaZPdyx31UrGIO3bZSlEjEaAleSEALw_wcB']}
    """
    # 40クラスお試し用URL
    import os
    import pandas as pd
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    df_label = pd.read_csv(os.path.join(BASE_DIR, '../knowledge/bert_model/models/keywords_40class.csv'))
    URL_DICT = {k: ['＜"{}"のURL1＞'.format(k), '＜"{}"のURL2＞'.format(k)] for k in df_label['keyword'].values}
    """

    def __init__(self):
        '''言語生成用クラス'''
        pass

    def generate_sentence(self, dialogue_act):
        '''
        行動タイプに基づいて文章を生成する
        
        Parameters
        -----------
        dialogue_act : dict
            次の行動を表す辞書
            キーにsys_act_type(行動タイプ)
        '''
        sys_act_type = dialogue_act['sys_act_type']
        
        # URLを提示する場合
        if sys_act_type == 'SUGGEST_GOODS':
            # PROBLEMにクラスラベルのリストが入っている場合
            sent = ''
            for problem in dialogue_act['PROBLEM']:
                sent += '\n{}という問題でお困りの方に、以下の商品・解決法をおすすめします。'.format(problem)
                # 症状と問題から解決法を提案する
                url_list = self.URL_DICT[problem]
                info = {'商品{}'.format(i+1): url for i, url in enumerate(url_list)}
                for name, url in info.items():
                    sent += '\n{}\n\t{}'.format(name, url)
            # PROBLEMにクラスラベルと確率の辞書が入っている場合
            # sent = ''
            # for problem, probable in dialogue_act['PROBLEM'].items():
            #     sent += '\n{} :  {:.5f}'.format(problem, probable)

        # デフォルトメッセージ
        elif sys_act_type == 'DEFAULT_MESSAGE':
            sent = 'ちょっと何言ってるかわからない'
            
        else:
            print('Error')
            sys.exit(-1)

        return sent
    