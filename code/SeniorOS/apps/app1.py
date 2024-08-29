from SeniorOS.lib.devlib import *
import SeniorOS.system.daylight as DayLight
import SeniorOS.system.pages as Pages
import SeniorOS.system.core as Core
import SeniorOS.system.radient as Radient
import gc
import os
import _thread
binmode=False
try:
    import ModRunner
    binmode=True
except:binmode=False
import SeniorOS.lib.log_manager as LogManager
source = "http://" + Core.Data.Get("text", "radienPluginsSource")
Log = LogManager.Log

def Main():
    pluginsNum = 0
    gc.enable()
    Core.FullCollect()
    DayLight.App.Style1('线上插件')
    Quit = Core.SharedVar.LoadQuit()
    Quit.value = False
    _thread.start_new_thread(Pages.LoadWait, (Quit, eval("[/Language('请稍等')/]"), False))
    try:
        pluginsList = ((Radient.Get(source + '/plugins/list.sros')[1]).split(';'))
        pluginsTip = ((Radient.Get(source + '/plugins/author.sros')[1]).split(';'))
        pluginsTip2 = ((Radient.Get(source + '/plugins/tip.sros')[1]).split(';'))
        Englist=(Radient.Get(source + '/plugins/list_English.sros'))[1].split(';')
        Log.Debug(len(pluginsList))
        Log.Debug(pluginsTip)
    except IndexError as e:
        Core.FullCollect()
        Quit.value = True
        __import__("sys").print_exception(e)
        Log.Error(str(e))
        return
    Quit.value = True
    del Quit
    Core.FullCollect()
    while not button_a.is_pressed():
        pluginsNum = DayLight.Select.Style2(pluginsList, pluginsTip, 18, False, "线上插件")
        if eval("[/GetButtonExpr('th')/]"):
            options = DayLight.ListOptions(['获取并运行', '插件详情', '缓存该插件'], False, "菜单")
            if options == 0:
                DayLight.VastSea.Off()
                DayLight.App.Style1('线上插件')
                DayLight.Text(eval("[/Language('请稍等')/]"), 5, 18, 2)
                DayLight.Text('由于适配问题，部分情况下A键无法退出，请尝试重启', 5, 36, 1)
                oled.show()
                Core.FullCollect()
                if binmode:
                    open("/SeniorOS/download/web_app.py","w").write(Radient.Get((''.join([str(x) for x in [source + '/plugins/main/web_app', pluginsNum + 1, '.sros']]))))
                    ModRunner.module_run("/SeniorOS/download/web_app.py")
                else:
                    oled.fill(0)
                    print(gc.mem_free())
                    exec(Radient.Get((''.join([str(x) for x in [source + '/plugins/main/web_app', pluginsNum + 1, '.sros']]))))
                    DayLight.VastSea.Off()
            if options == 1:
                DayLight.VastSea.Off()
                while not button_a.is_pressed():
                    DayLight.App.Style1(str(pluginsList[pluginsNum]))
                    DayLight.Text(str(pluginsTip2[pluginsNum]), 5, 18, 2)
                    # oled.DispChar(str(pluginsTip2[pluginsNum]), 5, 18, 1, True)
                    oled.show()
            if options == 2:
                DayLight.VastSea.Off()
                DayLight.app('线上插件')
                DayLight.Text(eval("[/Language('请稍等')/]"), 5, 18, 2)
                # oled.DispChar(eval("[/Language('请稍等')/]"), 5, 18, 1, True)
                DayLight.Text(eval("[/Language('正在进行操作')/]"), 5, 36, 2)
                oled.show()
                _response = Radient.Get((''.join([str(x) for x in [source + '/plugins/main/web_app', pluginsNum + 1, '.sros']])))
                try:
                    os.chdir("/SeniorOS/downloads")
                except:
                    os.mkdir("/SeniorOS/downloads")
                    os.chdir("/SeniorOS/downloads")
                with open(f"{Englist[pluginsNum+1]}.py","w") as file:
                    file.write(_response)
                os.chdir("/")
                oled.fill(0)
                DayLight.VastSea.Off()
                DayLight.VastSea.Off()

