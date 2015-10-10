package com.tinkeracademy.rvergis;

import net.minecraft.init.Blocks;
import net.minecraft.init.Items;
import net.minecraft.item.ItemStack;
import net.minecraftforge.common.DungeonHooks;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.registry.GameRegistry;

@Mod(modid = MyMod.MODID, version = MyMod.VERSION)
public class MyMod
{
    public static final String MODID = "rvergis_mymod";
    public static final String VERSION = "1.0";
    
    @EventHandler
    public void init(FMLInitializationEvent event)
    {
    	GameRegistry.addShapedRecipe(new ItemStack(Items.apple), new Object[]{"XXX", "XXX", "XXX", 'X', Blocks.leaves});
    	GameRegistry.addShapedRecipe(new ItemStack(Items.arrow, 2), new Object[]{"XY", "Z ", 'X', Items.flint, 'Y', Blocks.leaves, 'Z', Items.stick});
    	GameRegistry.addShapelessRecipe(new ItemStack(Blocks.wool, 1, 10), Blocks.wool, new ItemStack(Items.dye, 1, 5));
    	GameRegistry.addShapelessRecipe(new ItemStack(Items.diamond, 64), Blocks.dirt);
    	GameRegistry.addSmelting(Blocks.stone, new ItemStack(Blocks.stonebrick, 1), 2);
    	GameRegistry.addSmelting(Blocks.dirt, new ItemStack(Items.gold_ingot, 1), 2);
    }
}
